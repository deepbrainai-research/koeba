import argparse
import os
from pydub import AudioSegment
from scipy.io import wavfile

parser = argparse.ArgumentParser()
parser.add_argument('-youtube_id', '--youtube_id', help='youtube download id ex) vGHfSAk0FKg')
parser.add_argument('-save_path', '--save_path', default = 'audio/clip/', help='save path')

args = parser.parse_args()
YOUTUBE_ID = args.youtube_id
SAVE_PATH = args.save_path


if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)


input_video_path = os.path.join('audio/data', YOUTUBE_ID + '.m4a')
input_label_path = os.path.join('audio/labels', YOUTUBE_ID + '.txt')

start_times = []
end_times = []

file = open(input_label_path, 'r')
while True:
    line = file.readline()
    if not line:
        break

    
    start_time = str(line.split('\t')[0])
    end_time = str(line.split('\t')[1])

    start_times.append(start_time)
    end_times.append(end_time)
        


file.close()

print('Start Time List: ', start_times)
print('End Time List: ', end_times)


# m4a => wav
m4a_root = input_video_path
wav_root = os.path.join('audio/', 'temp.wav')
track = AudioSegment.from_file(m4a_root,  format= 'm4a')
file_handle = track.export(wav_root, format='wav')

for i in range(len(start_times)):
    
    start_time = float(start_times[i])
    end_time = float(end_times[i])
    
    sr, data = wavfile.read(wav_root)
    data_length = len(data)
    print(int(start_time * sr), int(end_time * sr))
    segment = data[int(start_time * sr):int(end_time * sr)]
    output_path = os.path.join('audio/clip', YOUTUBE_ID + '_S' + '%04d' %(int(start_time))  + '_E' + '%04d' %(int(end_time)) + '.wav')
    
    wavfile.write(output_path, sr, segment)
    
if os.path.exists(wav_root):
    os.remove(wav_root)




















