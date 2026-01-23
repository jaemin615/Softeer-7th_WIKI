### File structure

```
.
├── docker-compose.yml         # Spark 클러스터(Master, Worker, History) 서비스 정의
├── Dockerfile                 # Spark 및 PySpark 환경 구축을 위한 베이스 이미지 설정
├── entry.sh                   # 컨테이너 종류(Master, Worker, History)에 따른 프로세스 실행 스크립트 
├── conf/                      # Spark 환경 설정 파일
├── jobs/                      # 실행할 PySpark 분석 스크립트 (볼륨 마운트)
├── data/                      # 분석용 데이터 및 결과 파일 (볼륨 마운트)
├── logs/                      # Master, Worker 실행 로그 저장 (볼륨 마운트)
├── spark-events/              # History Server가 참조할 Event Log 저장 (볼륨 마운트)
└── submit_job.sh              # sample job scripts 실행파일
```


### Setting up volume directories for Docker containers
```bash
mkdir -p data logs spark-events
```

### Build docker image
```bash
docker-compose up -d
```
### Spark master web UI
http://localhost:8080/
### Spark worker1 web UI
http://localhost:8081/
### Spark worker2 web UI
http://localhost:8082/
### Spark history-server web UI
http://localhost:18080/


### Execute Sample job script(Pi_Estimation)
```bash
./submit_job.sh
```
The output (Pi is roughly 3.141440 ) will be printed in your shell

### Prepare text file for WordCount job
```bash
curl https://www.gutenberg.org/cache/epub/1661/pg1661.txt -o ./data/sherlock.txt
```

### Execute WordCount job
```bash
docker exec spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark/jobs/wordcount.py 
```
You can check the results in the data/output/ directory

