# KoEBA
## Overview

https://user-images.githubusercontent.com/123139173/213644804-783bfe33-bbd5-48be-9ec0-5628b6babbe0.mp4

**Korean Election Broadcast Addresses Dataset (KoEBA)** is a video dataset of Korean politicians’ speeches uploaded to YouTube. This dataset contains audio labels that show the intervals in which a person speaks, video labels that show scene transitions and some Python scripts for editing images and voices.

## Description
This dataset consists of videos of **104 politicians**. All video frames are **1080p high-resolution** images, which can be cropped to 256 or larger sizes(e.g. 512). Each video is **an average of 10 minutes long** enough to train the neural network. All videos also **contain voice**, so data can be used for learning lip-sync as well as face/voice synthesis networks. For your convenience, this page provides **Python scripts for downloading** videos and some **tools for editing videos**.


## Installation

```Python
conda create -n koeba python=3.7
conda activate koeba
pip install -r requirements.txt

```


## Download
### Download all videos
* download_video.py

This Python script allows you to download videos by reading YouTube links from the ‘download_list.csv’ file. You can choose one of three options to suit your purpose. The first is to download the video (with sound). The second is to download only the video (without sound), and the last is to download only the audio(m4a files).

```Python
# Option 1:
# save path: video/data/
python download_video.py --save_path video/data/


# Option 2: Only Video Download without Audio Sound
# save path: video/data/
python download_video.py --save_path video/data/ --only_video 1


# Option 3: Only Audio Donload
# save path: audio/data/
python download_video.py --save_path audio/data/ --only_audio 1
```

### Cautions
We provide video links and labels for easy downloading and editing. Note that please use it **for research purposes**. Inform that all videos are copyrighted by politicians and political parties. We only provide YouTube IDs and tools for downloading, but **not videos directly**. We are **not responsible for your commercial use or abuse of this video**. Please use it for public interest purposes. The provision of videos could be blocked for the personal reasons by politicians. In this case, remove the row from ‘download_list.csv’ and don’t use it.



## Python Scripts
### Convert .m4a to .wav

* m4a_to_wav.py

You can change the audio data in the form of m4a to wav file.

```Python
# input path: path for input m4a files
# save path: path for saving wav files

python m4a_to_wav.py --m4a_path audio/data/ --wav_path audio/wav/ 
```
### Clip
* clip_video.py

This Python script has the ability to **clip videos from label text**. Each line in text file is labeled with numbers. The first and second columns’ number means **start** and **end frame number**. The third column number means **the direction of the face**. When facing the front, the label is marked with number 1. Label with number 2 when the right side of the face is visible, and number 3 when the left side of the face is visible. If it is difficult to use as training data, label it as 0 (if the face is too small, there is no person, or the camera is moving). It is the front face, but if it is seen from another camera angle, it is marked with 4 instead of 1. Similarly, if taken from a different camera angle, mark 5 and 6 instead of 2 and 3.

e.g.) video/labels/0BUTu8NQpaw.txt
|  | start frame | end frame | face direction | scene notation | remark |
| --- | ---: | ---: | :---: | :---: | --- |
| line 1 | 0 | 140 | 0 (moving camera angle) | 018 | fade-in |
| line 2 | 141 | 495 | 4 (frontal face but different camera angle) | 019 |  |
| line 3 | 496 | 843 | 1 (frontal face) | 020 |  |
| line 4 | 844 | 1165 | 2 (right side face) | 021 |  |
| … | … | … | … | … | … |
| line N | 12460 | 12461 | 0 (too small face) | 033 | fade-out |

```Python
# If you want to clip only front side of face (front view = 1)
# save path: video/clip/xxxx.mp4
python clip_video.py --youtube_id xxxxx --view 1

# If you want to clip only right side of face (front view = 2)
# save path: video/clip/xxxx.mp4
python clip_video.py --youtube_id xxxxx --view 2

# If you want to clip all videos of front side face
# save path: video/clip/xxxx.mp4
python clip_all_video.py --view 1
```

* clip_audio.py

This Python script provides the ability to clip sounds from audio text labels. Find and clip only the parts of the human speech. The numbers in the first and second columns are the time when a politician starts speaking and the time(seconds) when he finishes speaking. Each segment was cut to within 10~11 seconds. The number in the third column is just scene number.

e.g.) audio/labels/0BUTu8NQpaw.txt

|  | start time (sec) | end time (sec) | scene notation |
| --- | ---: | ---: | :---: |
| line 1 | 5.920000 | 7.440000 | 002 |
| line 2 | 7.440000 | 10.170000 | 003 |
| line 3 | 10.390000 | 13.270000 | 004 |
| line 4 | 13.710000 | 15.070000 | 005 |
| … | … | … | … |
| line N | 414.380000 | 415.100000 | 223 |

```python
# If you want to clip specific m4a file 
# save path: audio/clip/xxxx.wav
python clip_audio.py --youtube_id YOUTUBE_ID

# If you want to clip all m4a files 
# save path: audio/clip/xxxx.wav
python clip_all_audio.py 
```

## About Data
This dataset is designed for video synthesis and speech synthesis. The following statistical filtering was performed to provide high-quality images and voices.

### Number of People
**A total of 104 politicians** will appear to present their policies.  

### Video length
To provide rich vocabulary and images, we found the sufficient length of videos. The videos have an average length of **about 11.5 minutes**(=691 seconds).  

* Statistic

| video length | the number of data |
| :---: | ---: |
| 4min ~ 6min  | 10 |
| 6min ~ 8min | 7 |
| 8min ~ 10min | 31 |
| 10min ~ 12min | 28 |
| 12min ~ 14min | 1 |
| 14min ~ 16min | 4 |
| 16min ~ 18min | 3 |
| 18min ~ 20min | 16 |
| 20min over | 4 |
| Total | 104 |  

### Clipping
In the case of audio data, the amplitude could be limited depending on the recording place, equipment, upload method and sampling method. If there are many truncated signals, the quality of the signal is degraded. Therefore, determine how many signals are saturated about the total audio signal length as **Clipping Ratio**. We remove data if they exceed a certain threshold. The threshold is $5\times10^{-5}$.  

$$\text{clipping ratio} = \frac{\text{the number of saturated signals}}{\text{total signal length}}$$


```python
def clip_ratio(wav_path):
    sr, data = wavfile.read(wav_path)
    data_length = len(data)
    abs_data = np.abs(data)
    clips = (abs_data == np.max(abs_data)) * 1
    num_clips = np.sum(clips)
    ratio = num_clips / data_length

    return ratio
```
* Statistic

| clipping ratio | the number of data |
| :---: | ---: |
| 1e-6 ~ 5e-5 | 3 |
| 1e-7 ~ 1e-6  | 11 |
| 1e-7 ~ 1e-6 | 14 |
| 1e-8 ~ 1e-7 | 76 |
| Total | 104 |  

### Frequency Spectrum & Sampling rate
Even if the sampling frequency is high, the actual recorded audio may be expressed in a much lower frequency range. Therefore, we analyzed the frequency spectrum in the audio in practice. We define the **effective frequency range** represented by truncating it from $-79dB$ when represented with a maximum of $0dB$ to a minimum of $ -80dB $. Depending on this effective frequency, we write the closest standard sampling frequency(16000Hz, 22050Hz, 24000Hz, 32000Hz, 44100Hz, etc.) called with an **effective sampling rate**. To provide sound in a rich frequency domain, signals less than 22050Hz are removed.

```python
def effectrive_freq(wav_path):
    y, sr = librosa.load(wav_path, sr=44100)
    n_fft = 2048
    S = librosa.stft(y, n_fft=n_fft, hop_length=n_fft // 2)
    D = librosa.amplitude_to_db(np.abs(S), ref=np.max)
    D_AVG = np.mean(D, axis=1)
    Threshold = -79
   
    FILT = (D_AVG > Threshold) * np.arange(D_AVG.shape[0])
    max_db_freq = np.max(FILT) / 1024 * sr / 2

    return max_db_freq

def effective_sr(eff_freq):
    frequency_candidate = np.array(
        [int(8000 / 2), 11025 / 2, int(16000 / 2), int(22050 / 2), int(24000 / 2), int(32000 / 2), int(44100 / 2),
         int(48000 / 2)])
    ARG = np.argmin(np.abs(frequency_candidate - eff_freq))

    return(int(frequency_candidate[ARG]) * 2)
```

* statistic

| effective frequency | the number of data |
| :---: | ---: |
| 9000Hz~10000Hz | 2 |
| 10000Hz~11000Hz | 4 |
| 11000Hz~12000Hz | 3 |
| 12000Hz~13000Hz | 6 |
| 13000Hz~14000Hz | 15 |
| 14000Hz~15000Hz | 15 |
| 15000Hz~16000Hz | 57 |
| over 16000Hz | 2 |
| Total | 104 |

| effective sampling rate | the number of data |
| :---: | ---: |
| 22050 | 8 |
| 24000 | 22 |
| 32000 | 74 |
| Total | 104 |  

## Licenses
Each video was posted on YouTube under the [Korean National Election Commission](https://www.nec.go.kr/site/nec/main.do). Metadata files, download script files, processing script files, and document files are available under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license(CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/). You can use, redistribute, and adjust the appropriate credit by citing our paper, indicating any changes you have made, and distributing derivative works under the same license. The fundamental copyright of the videos lies with the presenter and the publisher. This dataset is only designed to aid research not commercial. Therefore, we are not responsible for the conflict between video rights and commercial use.  


## Privacy
It is accessible to all people as a broadcast dataset for the election, but it can be banned at any time if politicians have privacy issues or interests. In such cases, please act as follows:

1. Remove the problematic videos and do not use them.

2. If you have any other problems with downloading, please notice by using e-mail [dunkin@deepbrainai.io](mailto:dunkin@deepbrainai.io)

## Contributors

[Seunghyun Lee](), [Sungwoo Park](), [Gyuhyeon Nam](), [Geumbyeol Hwang](), [Kihyeok Lee](), [Changjin Han](), [Jungjun Kim](), [Yoohyun Lee](), [Sunwon Hong](), and [Gyeongsu Chae]().

## Citation 

If you use koEBA dataset, please cite as
```plain
@misc{https://doi.org/10.48550/arxiv.2303.07697,
  doi = {10.48550/ARXIV.2303.07697},
  
  url = {https://arxiv.org/abs/2303.07697},
  
  author = {Hwang, Geumbyeol and Hong, Sunwon and Lee, Seunghyun and Park, Sungwoo and Chae, Gyeongsu},
  
  keywords = {Computer Vision and Pattern Recognition (cs.CV), Machine Learning (cs.LG), Image and Video Processing (eess.IV), FOS: Computer and information sciences, FOS: Computer and information sciences, FOS: Electrical engineering, electronic engineering, information engineering, FOS: Electrical engineering, electronic engineering, information engineering},
  
  title = {DisCoHead: Audio-and-Video-Driven Talking Head Generation by Disentangled Control of Head Pose and Facial Expressions},
  
  publisher = {arXiv},
  
  year = {2023},
  
  copyright = {arXiv.org perpetual, non-exclusive license}
}

```
