import argparse
import pandas as pd
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-csv_path', '--csv_path', default='download_list.csv', help='path of download_list.csv')
parser.add_argument('-save_path', '--save_path', default='video/data/', help='dir for saving videos')
parser.add_argument('-only_video', '--only_video', default = 0, help='if you want to download only video, make this option 1')
parser.add_argument('-only_audio', '--only_audio', default = 0, help='if you want to download only audio, make this option 1')
parser.add_argument('-sound_format', '--sound_format', default = 'm4a', help='webm is 48000 Hz, m4a is 44100 Hz')


args = parser.parse_args()
CSV_PATH = args.csv_path
SAVE_PATH = args.save_path
ONLY_VIDEO = args.only_video
ONLY_AUDIO = args.only_audio
AUDIO_FORMAT = args.sound_format

df = pd.read_csv(CSV_PATH)

for idx, row in df.iterrows():

    file_number, youtube_link, korean_name, roman_name, resolution, fps, audio_sr, video_opt, webm_opt, m4a_opt = row

    ## refresh the cache for safe download
    if (file_number % 3 == 0):
        command_refresh = 'youtube-dl --rm-cache-dir'
        res_refresh = subprocess.call(command_refresh, shell=True)

    audio_opt = None
    if AUDIO_FORMAT == 'm4a':
        audio_opt = m4a_opt
    else:
        audio_opt = webm_opt
    
    print(file_number, roman_name, youtube_link)
    

    ## download video + audio
    command = 'youtube-dl -o {save_path} -f {video_op}+{audio_op} ' \
              'https://www.youtube.com/watch?v={link}'.format(save_path=os.path.join(SAVE_PATH, youtube_link + '.mp4'),
                                                              video_op=str(video_opt),
                                                              audio_op=str(audio_opt),
                                                              link=youtube_link)
    
    ## download only video                                                          
    if ONLY_VIDEO:
        command = 'youtube-dl -o {save_path} -f {video_op} ' \
              'https://www.youtube.com/watch?v={link}'.format(save_path=os.path.join(SAVE_PATH, youtube_link + '.mp4'),
                                                              video_op=str(video_opt), link=youtube_link)
    ## download only audio
    if ONLY_AUDIO:
        command = 'youtube-dl -o {save_path} -f {audio_op} ' \
              'https://www.youtube.com/watch?v={link}'.format(save_path=os.path.join(SAVE_PATH, youtube_link + '.m4a'),
                                                              audio_op=str(audio_opt), link=youtube_link)
                                                              
    res = subprocess.call(command, shell=True)
    
    
