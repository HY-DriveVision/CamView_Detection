# You Only Look Once (Yolo)

* 분류 : 2D detection  
* 논문: "You Only Look Once: Unified, Real-Time Object Detection"
* 저자: Joseph Redmon∗
, Santosh Divvala, Ross Girshick, Ali Farhadi
* 출판년도: 2015
* github link : https://github.com/motokimura/yolo_v1_pytorch  
* 특징 : 기존 객체 탐지 기법들은 분류기를 활용하여 여러 위치에서 객체를 탐지하지만, YOLO는 이미지에서 객체의 경계 상자(bounding box)와 클래스 확률을 한 번에 예측하는 회귀 문제로 이 작업을 재정의한다. YOLO는 하나의 신경망이 전체 이미지를 처리하여 여러 객체의 경계 상자와 클래스 확률을 동시에 예측하는 방식으로 작동함.

### 주요 특징:

1. 속도: YOLO는 매우 빠르며, 기본 YOLO 모델은 초당 45프레임을 처리하고, 빠른 버전인 Fast YOLO는 초당 155프레임까지 처리할 수 있다. 이로 인해 실시간 객체 탐지가 가능함.
2. 전역적 추론: YOLO는 슬라이딩 윈도우나 지역 제안(region proposal) 방식을 사용하지 않고, 훈련과 테스트 과정에서 이미지를 전역적으로 처리하여 객체의 맥락 정보를 함께 학습한다.
3. 일반화 능력: YOLO는 자연 이미지에서 훈련된 후 다른 도메인(예: 예술 작품)에서도 우수한 성능을 보이며, 다양한 객체를 잘 일반화할 수 있다.

## YOLOv9  

* 논문: "YOLOv9: Learning What You Want to Learn Using Programmable Gradient Information"
* 저자: Chien-Yao Wang, I-Hau Yeh, and Hong-Yuan Mark Liao
* 출판년도: 2024
* github link : https://github.com/WongKinYiu/yolov9

24년에 나온 논문을 기반으로 한 v9. 기존의 yolo에서 어떤점이 달라졌는지를 통해서 깊이있는 이해가 가능할듯 하여 선택함.
