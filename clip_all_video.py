import argparse
import pandas as pd
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-csv_path', '--csv_path', default='download_list.csv', help='path of download_list.csv')
parser.add_argument('-view', '--view', default=1, help='1: front side face, 2: right side face, 3: left side face 0: cannot recognize, 4: front side face (annother angle) , 5: right side face (annother angle) , 6: left side face (annother angle)')
parser.add_argument('-save_path', '--save_path', default = 'video/clip/', help='save path')

args = parser.parse_args()
CSV_PATH = args.csv_path
SAVE_PATH = args.save_path
VIEW = args.view

df = pd.read_csv(CSV_PATH)

for idx, row in df.iterrows():

    file_number, youtube_link, korean_name, roman_name, resolution, fps, audio_sr, video_opt, webm_opt, m4a_opt = row

    

    command = 'python clip_video.py --youtube_id {youtube_id} --view {view}'.format(youtube_id=youtube_link, view=VIEW)
    
   
                                                              
    res = subprocess.call(command, shell=True)
    
    
