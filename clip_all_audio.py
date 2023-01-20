import argparse
import pandas as pd
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-csv_path', '--csv_path', default='download_list.csv', help='path of download_list.csv')
parser.add_argument('-save_path', '--save_path', default = 'audio/clip/', help='save path')

args = parser.parse_args()
CSV_PATH = args.csv_path
SAVE_PATH = args.save_path


df = pd.read_csv(CSV_PATH)

for idx, row in df.iterrows():

    file_number, youtube_link, korean_name, roman_name, resolution, fps, audio_sr, video_opt, webm_opt, m4a_opt = row

    

    command = 'python clip_video.py --youtube_id {youtube_id}'.format(youtube_id=youtube_link)
    
   
                                                              
    res = subprocess.call(command, shell=True)
    
    
