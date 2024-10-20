# You Only Look Once: Unified, Real-Time Object Detection
[URL : darknet](https://pjreddie.com/darknet/yolo/)
[github : yolo7](https://github.com/WongKinYiu/yolov7)
[yotube : yolo tutorial](https://www.youtube.com/watch?v=-gCB9Iotjs8)

## Absract
1. 이전의 object detection은 repurposes classifiers 감지
2. YOLO의 경우, 단일 신경망이 전체 이미지에서 bounding bos 와 클래스 확률을 한 번의 평가로 직접 예측합니다. 전체 탐지 파이프라인이 단일 네트워크이기 때문에 탐지 성능에 최적화
3. YOLO 모델은 초당 45 프레임으로 실시간으로 이미지를 처리
4. 위치 탐지 오류율이 높으나(자연탐지는 높지 않음) 속도면에서 DPM R-CNN 탐지 보다 뛰어남
   
## Introduction
1. (Figure1)기존 알고리즘의 복잡한 파이프라인 대신, Sing Convolutional Neural Network가 여러 bounding box와 해당상자의 Class 확율을 동시에 예측
3. YOLO는 훈련 및 테스트 시 전체 이미지를 보기 때문에 Class의 Appearace만 보는 것이 아닌 전체 맥락을 고려함
4. 일반화에 매우 강력함, 새로은 Data가 들어 왓을때 유연성이 높음
5. 정확도가 떨어지며 특히 정확하게 위치를 지정하는데 어려움을 겪음
6. Non-max suppression : 객체 탐지 알고리즘에서 사용되는 기법으로 여러개의 중복된 bounding box가 있을 때 가장 신뢰도가 높은 경계상자를 남기고 나머지를 제거하는 과정, 겹침의 정도는 IoU(Intersection Over Union 사용, 실제 vs 예측 bounding box, 신뢰도 높은거 제외 겹치는 bounding box 모두 제거)

## Unified Detection
1. 경계 상자는 (x, y, w, h, 신뢰도)로 구성, x, y = Bounding Box 중심의 좌표, w,h = Bounding Box의 넓이와 높이(이미지 전체에 대한 상대 비율), 신뢰도 = Class 존재 확률 X IOU(0~1사이값 교차영역비율 1에 가까워 질수록 실제 예측 유사)
2. (Figure2)입력 이미지를 SXS 그리드로 나누고 B개의 Bounding Box와 C(Conditioal Class Probability)로  S X S X( B * 5 + C(PASCAL VOC = 20 Classes)의 크기의 Tesnsor 로 생성- 객체를 탐지하는 역할
3. 각 Grid Cell은 B개의 bouning box와 해당상자에 대한 신뢰도 점수를 예측(수식)

## Network Design
1. CNN 구현 PASCAL VOC Data 활용
2. [PASCAL VOC](http://host.robots.ox.ac.uk/pascal/VOC/ "주석은 annotation file 형식, XML"
3. 24개의 컨볼루션 레이어와 그 뒤를 잇는 2개의 완전 연결 레이어로 구성. GoogLeNet이 사용한 인셉션 모듈 대신, Lin et al.의 방법과 유사하게 1 × 1 축소 레이어와 그 뒤를 잇는 3 × 3 컨볼루션 레이어를 사용(Figure 3)
4. Fast YOLO의 경우 24개 대신 9개

## Training
1. ImageNet 1000개 class 경쟁 데이터 셋에서 합성곱 사전 학습
2. 4개의 합성곱 계층과 두개의 FC Layer를 추가(합성곱 계층과 연결층을 결합)
3. 네트워크 입력 해상도 224 X 224 > 448 X 448로 올림
4. Image/Bounding Box 너비의 높이 정규화(0~1), Grid Cell의 x,y 좌표는 offset(0~1)
5. Activation Fuction은 Reaky ReLU
6. Loss = SSE(Sum squared error)
7. 위치오류 분류오류 다른 가중치 적용(5 vs 0.5)
8. (Loss 함수 수식 삽입)

## inference & limitation
1. PASCAL VOC를 통해 객체 탐지를 학습하고 성능 검증을 실시함
2. Non-max suppression으로 객체당 1개의 Bonding Box 만 선택
3. YOLOv1 각 Grid Cell이 두개의 상자만 예측, 하나의 클래스만 가짐
4. Bouding Box를 통해 예측함으로 새로운 데이터(가로세로비)가 다른 객체는 취약
5. 큰 Box와 작은 Box의 오류를 동일 주요 오류는 잘못된 위치예측임

