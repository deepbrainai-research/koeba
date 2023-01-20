import argparse
import os
from pydub import AudioSegment
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('-m4a_path', '--m4a_path', default='audio/data', help='directory path which have downloaded m4a files')
parser.add_argument('-wav_path', '--wav_path', default='audio/wav', help='dir for saving wav files')

args = parser.parse_args()
M4A_PATH = args.m4a_path
WAV_PATH = args.wav_path

m4a_files = os.listdir(M4A_PATH)
if not os.path.exists(WAV_PATH):
    os.mkdir(WAV_PATH)


for i in tqdm(range(len(m4a_files))):
    
    m4a_file = os.path.join(M4A_PATH, m4a_files[i])
    wav_file = os.path.join(WAV_PATH, m4a_files[i].split('.')[0] + '.wav')
    track = AudioSegment.from_file(m4a_file,  format= 'm4a')
    file_handle = track.export(wav_file, format='wav')


