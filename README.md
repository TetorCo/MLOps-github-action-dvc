# Try MLOps

* 제작 기간 : 2022-03-23 ~ 2022-03-28

## 프로젝트 기획 배경
MLOps라는 분야에 관심이 있었고 기존에 만들었던 ML 모델도 있었기 때문에 MLOps의 전체적인 작업의 흐름을 이해하고자 시작한 프로젝트입니다.

## MLops PipeLine

![CP2-Project drawio](https://user-images.githubusercontent.com/76984534/160883633-f19df56f-d610-48cb-8055-5de9ba742dc3.png)

## PipeLine 진행과정
*데이터는 미리 수집해놓은 데이터를 사용했습니다. (Feast와 Minio를 활용해서 Feature Store는 구축했지만 실제로 사용할 때 데이터가 추출되지 않는
오류때문에 사용하지 않았습니다.)*

1. 개발자가 코드를 수정하게 되면 ML 모델이 데이터로 학습을 하게 되고 
