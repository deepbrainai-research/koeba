import argparse
import os
import cv2

parser = argparse.ArgumentParser()
parser.add_argument('-youtube_id', '--youtube_id', help='youtube download id ex) vGHfSAk0FKg')
parser.add_argument('-view', '--view', default=1, help='1: front side face, 2: right side face, 3: left side face 0: cannot recognize, 4: front side face (annother angle) , 5: right side face (annother angle) , 6: left side face (annother angle)')
parser.add_argument('-save_path', '--save_path', default = 'clip/', help='save path')

args = parser.parse_args()
YOUTUBE_ID = args.youtube_id
VIEW = args.view
SAVE_PATH = args.save_path


if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)


input_video_path = os.path.join('video/data', YOUTUBE_ID + '.mp4')
input_label_path = os.path.join('video/labels', YOUTUBE_ID + '.txt')

start_frames = []
end_frames = []

file = open(input_label_path, 'r')
while True:
    line = file.readline()
    if not line:
        break

    
    start_frame = int(line.split('\t')[0])
    end_frame = int(line.split('\t')[1])
    direction = int(line.split('\t')[2])

    if direction == int(VIEW):
        start_frames.append(start_frame)
        end_frames.append(end_frame)
        


file.close()

print('Start Frame List: ', start_frames)
print('End Frame List: ', end_frames)


cap = cv2.VideoCapture(input_video_path)
len_cap = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
clip_num = 0
clip_max = len(start_frames)

if clip_max:
  
    for i in range(len_cap):
        ret, frame = cap.read()
        start_num = start_frames[clip_num]
        end_num = end_frames[clip_num]
        
        if (start_num == i):
            OUTPUT = os.path.join(SAVE_PATH, YOUTUBE_ID + '_S' + '%06d'%(start_num) + '_E' + '%06d'%(end_num) + '_V' + str(VIEW) +'.mp4')
            output_video = cv2.VideoWriter(OUTPUT, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))
            print(OUTPUT)
        
        
        if (start_num <= i) & (i <= end_num):
            output_video.write(frame)
        
        if (end_num == i):
            clip_num += 1
            
        
        if clip_num == clip_max:
            break
        
        




















