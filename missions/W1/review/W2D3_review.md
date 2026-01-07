## W2M6

### docker

#### 콘솔에서 실행

docker run 옵션

-d (detach),컨테이너를 백그라운드에서 실행
-it,-i(interactive)와 -t(tty)의 조합. 컨테이너 내부 터미널로 직접 진입할 때 사용
--name,컨테이너에 이름을 부여
--rm,컨테이너가 종료되면 자동으로 삭제
-p 호스트포트:컨테이너 포트  포트포워딩 설정
--network 컨테이너가 사용할 네트워크 지정
-e 컨테이너에서 사용할 환경변수 설정
-v 데이터 볼륨 마운트

base image - ubuntu latest lts version (24.04)

`docker run -it -p 8888:8888 --name ubuntu-jupyter ubuntu:24.04 /bin/bash`

패키지 목록 업데이트 및 Python 설치
`apt-get update`
`apt-get install -y python3 python3-pip python3-dev`

필요한 라이브러리 설치
`install jupyterlab pandas numpy matplotlib wordcloud`

주피터 랩 실행 테스트
`jupyter lab --ip=0.0.0.0 --port=8888 --allow-root --no-browser`

#### 도커 파일 작성

docker는 각 줄을 실행한 결과를 캐싱하므로  만약 특정 코드 부분이 수정되면 그 아래 줄들만 다시 실행됨

ubuntu의 대화형 프롬프트 방지
ENV DEBIAN_FRONTEND=noninteractive

ubuntu 24.04 부터는 pip 설치 시 venv 사용 or --break-system-packages 옵션
