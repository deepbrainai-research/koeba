import gc
import math
import os
import shutil
import subprocess
import warnings
from argparse import ArgumentParser
from glob import glob
from pprint import pprint

import imageio
import numpy as np
import torch
from facenet_pytorch import MTCNN
from skimage import img_as_ubyte
from skimage.transform import resize
from tqdm import tqdm

warnings.filterwarnings("ignore")

device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn = MTCNN(
    min_face_size=64,
    post_process=False,
    select_largest=False,
    selection_method='largest_over_threshold',
    keep_all=True,
    device=device
)

def compute_bbox(start, end, fps, tube_bbox, inp, image_shape,filename, encoder='x264'):
    left, top, right, bot = tube_bbox
    h, w = bot - top, right - left

    start = start / fps
    end = end / fps
    time = end - start

    scale = f'{image_shape[0]}:{image_shape[1]}'

    # Center crop when width is larger than height
    if w > h:
        left += (w - h) // 2
        w = h

    encoder_params = 'libx264'
    if encoder == 'x265':
        encoder_params = 'libx265 -x265-params log-level=warning'
    return f'ffmpeg -i {inp} -ss {start} -t {time} -c:v {encoder_params} -crf 18 -preset fast -filter:v "crop={w}:{h}:{left}:{top}, scale={scale}:force_original_aspect_ratio=decrease,pad={scale}:-1:-1:color=black" {filename} -loglevel warning -y'

def read_video(path, write_to_disk=False, tmp_dir='tmp'):
    reader = imageio.get_reader(path)
    fps = reader.get_meta_data()['fps']

    if not write_to_disk:
        video = []
        try:
            for im in reader:
                video.append(im)
        except Exception as e:
            print(e)
            pass
        reader.close()
        return video, fps
    else:
        os.makedirs(tmp_dir, exist_ok=True)
        subprocess.call(f'ffmpeg -i {path} {tmp_dir}/%05d.jpg -loglevel warning', shell=True)
        reader.close()
        return fps

def join(tube_bbox, bbox):
    xA = min(tube_bbox[0], bbox[0])
    yA = min(tube_bbox[1], bbox[1])
    xB = max(tube_bbox[2], bbox[2])
    yB = max(tube_bbox[3], bbox[3])
    return (xA, yA, xB, yB)

def bb_intersection_over_union(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

def extract_bbox_lm(frame, increase=0.0, y_shift=0.0):
    if max(frame.shape[0], frame.shape[1]) > 640:
        scale_factor =  max(frame.shape[0], frame.shape[1]) / 640.0
        frame = resize(frame, (int(frame.shape[0] / scale_factor), int(frame.shape[1] / scale_factor)))
        frame = img_as_ubyte(frame)
    else:
        scale_factor = 1

    try:
        boxes, probs, points = mtcnn.detect(frame, landmarks=True)
        _, _, lm = mtcnn.select_boxes(boxes, probs, points, frame)
        lm = lm[0]
    except Exception as e:
        print('Cannot detect landmarks from image', e)

    eye_left     = lm[0]
    eye_right    = lm[1]
    eye_avg      = (eye_left + eye_right) * 0.5
    eye_to_eye   = eye_right - eye_left
    mouth_left   = lm[3]
    mouth_right  = lm[4]
    mouth_avg    = (mouth_left + mouth_right) * 0.5
    eye_to_mouth = mouth_avg - eye_avg

    x = eye_to_eye - np.flipud(eye_to_mouth) * [-1, 1]
    x /= np.hypot(*x)
    x *= max(np.hypot(*eye_to_eye) * 2.0, np.hypot(*eye_to_mouth) * (1.8 + increase))
    y = np.flipud(x) * [-1, 1]
    c0 = eye_avg + eye_to_mouth * (0.1 + y_shift)

    quad = np.stack([c0 - x - y, c0 - x + y, c0 + x + y, c0 + x - y])
    top = np.min(quad[:,1])
    bot = np.max(quad[:,1])
    left = np.min(quad[:,0])
    right = np.max(quad[:,0])

    bbox_h, bbox_w = bot - top, right - left

    if bbox_h > bbox_w:
        top, bot = round(top), round(bot)
        width_increase = ((bot - top) - bbox_w) / 2
        left = round(left - width_increase)
        right = round(right + width_increase)
    elif bbox_w > bbox_h:
        left, right = round(left), round(right)
        height_increase = ((right - left) - bbox_h) / 2
        top = round(top - height_increase)
        bot = round(bot + height_increase)

    top, bot, left, right = max(0, top), min(bot, frame.shape[0]), max(0, left), min(right, frame.shape[1])
    bbox = [[left, top, right, bot]]
    return (np.array(bbox) * scale_factor).astype(int)

def crop(inp, image_shape=(256, 256), increase=0.0, y_shift=0.0, iou_with_initial=0.25, min_frames=150, filename='crop.mp4', tmp_dir='tmp', encoder='x264'):
    fps = read_video(inp, write_to_disk=True, tmp_dir=tmp_dir)
    video_frame_paths = sorted(glob(os.path.join(tmp_dir, '*.jpg')))

    trajectories = []

    try:
        for i, path in enumerate(tqdm(video_frame_paths, desc='Crop video')):
            if i > 0 and i < len(video_frame_paths) - 1 and i % (fps // 4) != 0: continue
        
            frame = imageio.imread(path)
            bboxes =  extract_bbox_lm(frame, increase=increase, y_shift=y_shift)
            # print(i, bboxes)
            if len(bboxes) == 0:
                print(path) ## dunkin edit
                continue
            ## For each trajectory check the criterion
            valid_trajectories = []

            for trajectory in trajectories:
                tube_bbox = trajectory[0]
                intersection = 0
                for bbox in bboxes:
                    intersection = max(intersection, bb_intersection_over_union(tube_bbox, bbox))

                if intersection > iou_with_initial:
                    valid_trajectories.append(trajectory)

            trajectories = valid_trajectories

            ## Assign bbox to trajectories, create new trajectories
            for bbox in bboxes:
                intersection = 0
                current_trajectory = None
                for trajectory in trajectories:
                    tube_bbox = trajectory[0]
                    current_intersection = bb_intersection_over_union(tube_bbox, bbox)

                    if intersection < current_intersection and current_intersection > iou_with_initial:
                        intersection = bb_intersection_over_union(tube_bbox, bbox)
                        current_trajectory = trajectory

                ## Create new trajectory
                if current_trajectory is None:
                    trajectories.append([bbox, bbox, i, i])
                else:
                    current_trajectory[3] = i
                    current_trajectory[1] = join(current_trajectory[1], bbox)

    except IndexError as e:
        raise (e)

    commands = []
    for i, (bbox, tube_bbox, start, end) in enumerate(trajectories):
        # print('c', i)
        if (end - start) > min_frames:
            command = compute_bbox(start, end, fps, tube_bbox, inp=inp, image_shape=image_shape, filename=filename, encoder=encoder)
            commands.append(command)
            
    #print(1111111111111111111, commands)
    subprocess.call(commands[-1], shell=True)

    del trajectories
    del current_trajectory
    del valid_trajectories
    gc.collect()

    shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--image_shape", default=(256, 256), type=lambda x: tuple(map(int, x.split(','))),
                        help="Image shape")
    parser.add_argument("--increase", default=0.1, type=float, help='Increase bbox by this amount')
    parser.add_argument('--y-shift', default=1.0, type=float, help='Increase y-shift by this amount')
    parser.add_argument("--iou_with_initial", type=float, default=0.25, help="The minimal allowed iou with inital bbox")
    parser.add_argument("--inp", required=True, help='Input image or video')
    parser.add_argument("--min_frames", type=int, default=15,  help='Minimum number of frames')
    parser.add_argument("--filename", type=str, default='crop.mp4', help='Output filename')
    args = vars(parser.parse_args())
    pprint(args)

    if os.path.isdir(args['inp']):
        video_paths = []
        for ext in ('*.mp4', '*.MP4', '*.mov', '*.MOV'):
            video_paths.extend(glob(os.path.join(args['inp'], ext)))
        video_paths = sorted(video_paths)
    else:
        video_paths = [args['inp']]

    print('video_paths', video_paths)

    for _, path in enumerate(tqdm(video_paths)):
        tmp_dir = os.path.join('tmp', os.path.basename(path))           
        crop(
            image_shape=args['image_shape'],
            increase=args['increase'],
            y_shift=args['y_shift'],
            iou_with_initial=args['iou_with_initial'],
            inp=args['inp'],
            min_frames=args['min_frames'],
            filename=args['filename'],
            tmp_dir=tmp_dir)
