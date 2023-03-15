# KoEBA
## 대한민국 선거 방송연설 데이터 세트

https://user-images.githubusercontent.com/123139173/213644804-783bfe33-bbd5-48be-9ec0-5628b6babbe0.mp4


**대한민국 선거 방송 연설 데이터 세트(Korean Election Broadcast Addresses Dataset, koEBA)** 는 유튜브에 업로드 된 대한민국 정치인 연설을 담은 비디오 데이터세트입니다. 이 데이터 세트는 사람이 말하는 구간에 대한 시간 레이블과, 장면의 전환을 보여주는 비디오 레이블을 담고 있습니다. 또한 편의를 위해 비디오 및 음성을 편집할 수 있는 Python 스크립트를 제공합니다.

**If you want an English translation version, please click** [README_English](https://github.com/deepbrainai-research/koeba/blob/master/README_English.md).


## 요약
* 이 데이터 세트는 **약 104명**의 정치인에 대한 연설 비디오를 담고있습니다.
* 모든 비디오는 고해상도 품질을 제공하기 위해서 **1080p를 선별**하였습니다. 따라서 256x256, 512x512 혹은 더 큰 사이즈까지 가공 크롭이 가능합니다.
* 각 비디오는 평균적으로 **10분 이상의 길이** 를 가지고 있어 뉴럴 네트워크를 학습하기에 충분합니다.
* 모든 비디오는 **음성이 함께** 있습니다. 따라서 립싱크 모델 및 얼굴/음성 합성 테스크에 모두 이용하실 수 있습니다. 
* 각 영상을 다운로드 받을 수 있는 기능과 영상을 편집할 수 있는 Python 스크립트를 제공합니다.

## 설치

```Python
conda create -n koeba python=3.7
conda activate koeba
pip install -r requirements.txt
```


## 다운로드

### 비디오 전체 다운받기
* download_video.py
이 Python 스크립트는 ‘download_list.csv’ 파일로부터 YouTube link를 읽어서 비디오를 다운로드 받을 수 있도록 해 줍니다. 총 세 가지의 다운로드 옵션이 있습니다. 목적에 맞는 옵션을 선택하여 다운로드 받으시면 됩니다. 첫 번째 옵션은 비디오와 음성 모두 같이 다운로드 받는 방식입니다. 이밖에 소리는 제외하고 영상만 다운로드 받는 방식, 영상은 제외하고 소리만 다운로드 하는 방식(.m4a)이 있습니다.

```Python
# Option 1: 영상과 비디오를 함께 다운로드
python download_video.py --save_path video/data/


# Option 2: 영상만 다운로드하기
python download_video.py --save_path video/data/ --only_video 1


# Option 3: 음성만 다운로드하기
python download_video.py --save_path audio/data/ --only_audio 1
```

### 주의사항
이 데이터세트는 쉽게 다운로드하고 편집할 수 있도록 비디오 링크와 레이블만을 제공합니다. 오직 공익을 위한 연구를 목적으로 제공하고 있음을 명심하십시오. [공직선거법 제279조](https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B3%B5%EC%A7%81%EC%84%A0%EA%B1%B0%EB%B2%95)에 의거하여 모든 비디오의 저작권은 각급 선거관리 위원회에 있습니다.

따라서 영상을 직접 배포하지 않고, 유튜브 ID와 다운로드 할 수 있는 기능들만을 제공합니다. 상업적인 목적이나 비디오의 오용을 통한 문제에 대해서 책임지지 않습니다. 공익을 목적으로만 이용해주십시오. 또한 정치인 개인의 사유로 인해 영상의 접근에 문제가 생기는 경우 ‘download_list.csv’에서 해당 링크를 지운 후 사용해주시기 바랍니다.



## 편집용 Python 스크립트

### 영상 클립

* clip_video.py

이 Python 스크립트는 txt파일의 레이블로부터 비디오 구간을 클립하는 기능을 제공합니다. 비디오는 수많은 이미지 프레임들의 집합으로 이루어져있습니다. 레이블 파일(.txt)의 각 줄에는 숫자들이 적혀있습니다. 첫 번째 열과 두번 째 열의 숫자는 각각 시작 프레임 숫자와 끝나는 프레임 숫자입니다. 세 번째 열의 숫자는 머리가 향하는 방향을 의미합니다. 정면을 바라보는 경우에는 숫자 1, 오른쪽 얼굴이 보이는 경우는 숫자 2, 얼굴의 왼쪽면이 보이는 경우는 숫자 3으로 레이블링하였습니다. 숫자가 0인 경우에는 화면이 움직이거나, 화자의 얼굴이 너무 작아서 보이지 않아 사용할 수 없는 경우를 의미합니다. 똑같이 정면을 바라보고 있으나 다른 장면인 경우에는(배경이 다르거나, 다른 카메라로 촬영하는 경우 등) 숫자 4로 표시하였습니다. 오른쪽 얼굴과 왼쪽 얼굴의 경우에도 동일하게 2와 3 대신에 5와 6으로 레이블 작업을 하였습니다.

ex) video/labels/0BUTu8NQpaw.txt

|  | 시작 프레임 | 끝 프레임 | 머리방향 | 장면 번호 | 주석 |
| --- | --- | --- | --- | --- | --- |
| 1 행 | 0 | 140 | 0 (카메라 앵글이 움직임) | 018 | fade-in |
| 2 행 | 141 | 495 | 4 (정면을 바라봄, 다른 앵글에서 촬영) | 019 |  |
| 3 행 | 496 | 843 | 1 (정면) | 020 |  |
| 4 행 | 844 | 1165 | 2 (얼굴 오른쪽면) | 021 |  |
| … | … | … | … | … | … |
| N 행 | 12460 | 12461 | 0 (얼굴이 너무 작음) | 033 | fade-out |



### 음성 클립

• clip_audio.py

이 Python 스크립트는 txt파일의 레이블로부터 말하는 구간을 클립하는 기능을 제공합니다. 첫 번째 열과 두 번째 열은 말을 시작한 시간과 말을 끝마친 시간을 의미합니다. 각 구간은 약 10~11초 이내로 분할하였습니다. 

ex) audio/labels/0BUTu8NQpaw.txt

|  | 시작 시각 (초) | 마친 시각(초) | 장면 번호 |
| --- | --- | --- | --- |
| 1 행 | 5.920000 | 7.440000 | 002 |
| 2 행 | 7.440000 | 10.170000 | 003 |
| 3 행 | 10.390000 | 13.270000 | 004 |
| 4 행 | 13.710000 | 15.070000 | 005 |
| … | … | … | … |
| N 행 | 414.380000 | 415.100000 | 223 |

```python
# 특정 m4a 파일의 음성 클립을 원할 때
# 저장위치: audio/clip/xxxx.wav
python clip_audio.py --youtube_id YOUTUBE_ID

# 모든 m4a 파일의 음성 클립을 원할 때 
# 저장위치: audio/clip/xxxx.wav
python clip_all_audio.py 
```
## 데이터 통계


이 데이터세트는 높은 품질의 영상과 음성을 제공하기 위해  다음과 같은 통계적 특성을 반영합니다. 

### 사람 수

총 104명의 정치인이 등장하여 연설합니다.

### 비디오 길이

평균적으로 약 11.5분(691초)의 길이를 가지고 있습니다. 따라서 풍부한 어휘와 이미지를 제공할 수 있습니다.
| 비디오 길이 | 데이터수 |
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


### 신호 클리핑

음성데이터의 경우 녹화 환경에 따라서 신호가 잘려나가는 현상이 빈번하게 발생합니다. 이런 현상이 빈번할수록 왜곡이 심하고 저품질의 데이터가 되어 합성 결과에 안좋은 영향을 미칠 수 있습니다. 따라서 우리는 포화된 신호의 비율이 $5\times10^{-5}$ 를 넘어가지 않는 데이터들로 엄선하였습니다.

$$
\text{clipping ratio} = \frac{\text{the number of saturated signals}}{\text{total signal length}}
$$

| 클리핑 비율 | 데이터 수 |
| --- | --- |
| 1e-6 ~ 5e-5 | 3 |
| 1e-7 ~ 1e-6  | 11 |
| 1e-7 ~ 1e-6 | 14 |
| 1e-8 ~ 1e-7 | 76 |
| 총계 | 104 |

### 주파수 스팩트럼

샘플링 된 주파수가 높더라도, 실제로 표현된 오디오 신호는 훨씬 낮은 주파수의 범위에서 기록되었을 수 있습니다. 따라서 음성 신호의 스펙트럼 분석을 통해 유효한 음성 스펙트럼을 계산하고, 이때 최적의 샘플링 주파수를 계산합니다. 음성에서 주로 사용하는 샘플링 주파수는 16000Hz, 22050Hz, 24000Hz, 32000Hz, 44100Hz 입니다. 유효 샘플링 주파수가 22050Hz 미달인 경우의 데이터는 제거하였습니다. 각 음성신호의 유효 주파수는 스펙트럼의 강도를 최대 0dB, 최소 -80dB로 표현하였을 때 -79dB까지의 신호를 유효 주파수로 계산하였습니다. 이 값의 두 배에서 가까운 주파수를 적정 샘플링 주파수로 계산하였습니다.

| 유효 주파수 범위 | 데이터 수 |
| --- | --- |
| 9000Hz~10000Hz | 2 |
| 10000Hz~11000Hz | 4 |
| 11000Hz~12000Hz | 3 |
| 12000Hz~13000Hz | 6 |
| 13000Hz~14000Hz | 15 |
| 14000Hz~15000Hz | 15 |
| 15000Hz~16000Hz | 57 |
| over 16000Hz | 2 |
| 총계 | 104 |

| 유효 샘플링 주파수 | 데이터 수 |
| --- | --- |
| 22050 | 8 |
| 24000 | 22 |
| 32000 | 74 |
| 총계 | 104 |

## 딥페이크 연구용 데이터 제공

딥페이크는 인공지능 기술은 진짜처럼 보이는 조작된 영상을 생성하는 기술입니다. 만들어진 딥페이크 영상은 진위 판별이 어렵기때문에 선동이나 협박에 사용되는 경우 큰 피해를 야기할 수 있습니다. 최근 인공지능 기술의 발전에 따라 딥페이크를 이용한 범죄의 위험도 증가하고 있습니다. 이러한 사회적 문제를 방지하기 위해 [딥브레인AI](https://www.deepbrain.io/ko/home)는 가짜 딥페이크 영상을 판별하는 기술 개발에도 박차를 가하고 있습니다.

우리는 딥페이크 영상 판별에 도움을 줄 수 있도록 해당 데이터로 학습하여 합성한 가짜 정치인 영상을 보유하고 있습니다. 합성된 가짜 영상이 악의적인 목적에 의해 사용되는 것을 방지하고, 탐지 기술 연구를 통해 사회적 공익을 도모할 분들에 한정하여 합성 영상 데이터 세트를 제공합니다.

다음 [서약서](https://docs.google.com/forms/d/1OhV1QGPSjHk-LL271jV5cMirzmmKyy45H4nL9xb3wWA/edit)에 응해주시면 심사를 통하여 데이터를 제공해드립니다. 


# 라이센스


모든 영상은 중앙선거관리위원회의 공직선거법에 의거하여 유튜브에 게시되어있습니다. 우리가 제공하는 메타데이터 파일, 다운로드 및 편집 스크립트는 [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International(CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)을 따릅니다. 우리 논문을 인용하고 해당 라이선스의 이용법을 준수함으로써  적절하게 재사용, 배포, 변형, 편집 등이 가능합니다. 비상업적 용도와 연구를 목적으로만 배포를 허락하기떄문에 비디오의 저작권이나 상업적 이용시 이해충돌에 대해서 법적 책임을 지지 않습니다.

# 인용

다음 데이터를 사용하시는 경우 아래를 인용해주세요.
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


# 참여자


[이승현](), [박성우](), [남규현](), [황금별](), [이기혁](), [한창진](), [김정준](), [이유현](), [홍순원](), [채경수]().

