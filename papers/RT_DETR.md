# DETRs Beat YOLOs on Real-time Object Detection
#### [논문주소](https://arxiv.org/abs/2304.08069)


## Abstract
#### YOLO는 NMS (Non-Maximum Suppression)로 인해 속도가 저하되고 정확성이 낮아짐. DETR 계열은 NMS가 필요없지만, 높은 연산 비용으로 실시간 사용이 어려움
#### RT-DETR은 실시간 DETR제안, 하이브리드 인코더와 최소화 쿼리 선택 기법 도입

## 제안모델 
### ![Figure4](images/RT_DETR_F4.png)
### 하이브리드 인코더
#### Intra-Scale Interaction(AIFI) : 스케일의 특징을 독립적으로 처리, 상위 레이어에서만 Intra Scale 상호작용 사용, 하나의 특정 스케일 내에서만 상호작용 시킴, 특정 스케일(저해상도(큰스케일) 물체의 전체적인 형태 포착 가능, 작은 스케일은 물체의 구체적은 텍스쳐와 디테일 더욱 잘 학습), 저해상도 주요 스케일에서만 상호작용, 고해상도는 모든 스케일에 상호작용 안함 그래서 빠름. 기존의 DETR은 모든 해상도와 상호 작용 해야됨

#### Cross Scale Convolutional Feature Fusion(CCFF) : 서로 다른 스케일의 정보를 통합하여 저해상도와 고해상도의 정보가 조화를 이루어 학습할 수 있음

### Uncertainty-Minimal Query Selection
#### 에피스테믹 불확실성(epistemic uncertainty)**을 정의하여, 분류 점수와 위치 신뢰도 간 차이를 측정 이 불확실성을 최소화하는 방향으로 쿼리를 최적화 이를 통해, 초기 단계에서 고품질의 쿼리를 디코더에 제공할 수 있으며, 결과적으로 모델의 전체 정확도가 향상

### Flexible Speed Tuning(디코더레이어 수 조정)
#### 정확도와 속도 Trade Off

## 효과
### RT-DETR-R101 모델:
#### 54.3% AP와 74 FPS를 달성
#### 기존의 DETR 계열 모델 중 하나인 DINO-Deformable-DETR-R50과 비교했을 때, 정확도는 2.2% AP 더 높고, 속도는 약 21배 빠름 (5 FPS에서 108 FPS로 증가).


