# Do it! MLOps

* 제작 기간 : 2022-03-23 ~ 2022-03-28

## 프로젝트 기획 배경
MLOps라는 분야에 관심이 있었고 기존에 만들었던 ML 모델을 활용해서 MLOps의 전체적인 작업의 흐름을 이해하고자 시작한 프로젝트입니다.

## First MLOps PipeLine
![final-mlops-pipeline](https://user-images.githubusercontent.com/76984534/160886227-91839fd4-913e-4727-a2b6-72fc77451f3e.png)

## First MLOps PipeLine 진행과정
1. Hadoop에서 .parquet를 받아서 Feast에 저장하고 Feast Server를 띄우는 대신 Docker Container를 이용해서 Minio에 데이터를 저장합니다.
2. 개발자가 코드를 수정했을 때 Minio로 부터 데이터를 받아서 ML 모델이 학습을 진행하고 Model Serving API에 적용한 다음 GitHub에 Commit합니다.
3. GitHub에 Commit하는 과정을 Jenkins가 자동으로 감지해서 Virtual Machine(서버)에 적용해서 Docker Container로 API를 구동합니다.
4. Locust가 해당 Docker Container를 시뮬레이션 하게 되고 이 때 발생한 Metrics를 Prometheus가 수집하게 됩니다. (Jenkins의 Metrics도 같이 수집합니다.)
5. Promtheus가 수집한 Metrics를 Grafana로 연동해 ML 모델 성능과 Jenkins의 성능을 모니터링 할 수 있는 DashBoard를 생성하게 됩니다.

## 프로젝트 진행 중 발생한 문제점
* Feast와 Minio를 활용하여 Feature Store를 구축했으나 실제로 모델이 학습을 하기 위해서 Feature를 추출하게 되면 Entity Key만 추출되는 에러가 발생했습니다. -> 실시간으로 수집해야 하는 데이터는 아니므로 사전에 수집한 데이터를 활용해서 진행했습니다.
* dvc repro를 실행할 때 에러가 자꾸 발생했습니다. -> 원본 csv 파일을 한 번 더 저장하는 방식으로 해결
* Locust가 시뮬레이션을 할 때 Faliure가 96~98%에 달하는 것으로 보아 ML 모델에 문제가 있거나 시뮬레이션 과정에서 문제가 있는 것 같습니다.
* 만약에 수정한 모델이 이전의 모델보다 좋지 않다면? -> 이런 상황을 방지하기 위해서 Model Testing과 Model Serving을 나누어 주었습니다.

## Final MLops PipeLine
* 위에서 언급한 문제점 때문에 Feast와 Minio가 제외되었음을 알 수 있습니다.
![CP2-Project drawio](https://user-images.githubusercontent.com/76984534/160883633-f19df56f-d610-48cb-8055-5de9ba742dc3.png)

## Final MLOps PipeLine 진행과정

1. 개발자가 코드를 수정하게 되면 ML 모델이 데이터로 학습을 하게 되고 학습한 모델을 FastAPI을 사용하여 모델의 성능을 테스트하는 API를 생성합니다.
2. GitHub에 Commit하는 과정을 Jenkins가 자동으로 감지해서 Virtual Machine(서버)에 적용해서 Docker Container로 API를 구동합니다.
3. Locust가 해당 Docker Container를 시뮬레이션 하게 되고 이 때 발생한 Metrics를 Prometheus가 수집하게 됩니다. (Jenkins의 Metrics도 같이 수집합니다.)
4. Promtheus가 수집한 Metrics를 Grafana로 연동해 ML 모델 성능과 Jenkins의 성능을 모니터링 할 수 있는 DashBoard를 생성하게 됩니다.
5. 만약 수정한 모델의 성능이 이전 모델보다 성능이 좋다면 Model Serving API의 ML 모델을 수정해줍니다.

## 내부 디렉토리 구조
```
itbi
┖ .dvc
┖ .github
  ┖ workflows
    ┖ train.yaml  # github actions을 수행하는 파일
┖ app
  ┖ static			# 웹 페이지에 사용할 이미지
  ┖ templates		# 웹 페이지를 띄우는 html
  ┖ main.py     # flask 구동 파일
create_csv_with_dvc.py  # 에러때문에 생성해준 파일
docker-compose.yml      # 컨테이너를 실행하기 위한 파일
Dockerfile              # 도커 파일
dvc.lock
dvc.yaml
dvc_players_stats.csv
Jenkinsfile             # Jenkins가 감지하기 위한 파일
metrics.json            # ML 모델의 metrics 파일
player_stats.csv        # 원본 csv 파일
requirements.txt        # 필요한 라이브러리 모음
script.groovy           # Jenkins 파일과 연동
train.py                # ML 모델이 학습하는 파일
```

## 사용 프로그램
* Feature Store
  *  Feast : Feature Store의 한 종류로 외부 프로그램과 통합하기 쉬워서 사용했습니다.
  *  Minio : Feast의 원천 데이터를 저장하기 위해 사용했습니다.
  *  Mlflow : ML 모델의  .pkl, parameters 등을 저장하기 위해 사용했습니다.
* CI/CD PipeLine
  * GitHub Actions : Workflow을 구현하기 위해서 사용했고, CML이나 DVC 같은 오픈소스와 연동했습니다.
  * Jenkins : 서버에서 따로 명령어를 입력하지 않아도 자동으로 적용이 되게끔 했습니다.
* Model Monitoring
  * Prometheus : Locust나 Jenkins에 발생한 Metrics를 수집합니다.
  * Locust : Model Testing API를 시뮬레이션 합니다.
  * Grafana : Prometheus에서 받은 Metrics를 DashBoard를 통해서 시각화 해줍니다.

## 앞으로의 발전 과제
* Model을 수정해서 Locust에서 시뮬레이션 결과가 나오게끔 수정해서 DashBoard에 띄울 수 있게 수정
* Kubeflow로 최적의 Hyperparameters 찾아내기
