### Project Structure
```
. 
├── configs/ 
├── job/
│	└── mapper.py 
│	└── reducer.py 
│   └── negative-words.txt 
│ 	└── positive-words.txt 
│ 	└── training.1600000.processed.noemoticon.csv
├── Dockerfile
├── docker-compose.yml 
└── start_hadoop.sh 
```
### Tweets data

[Sentiment140 dataset with 1.6 million tweets](https://www.kaggle.com/datasets/kazanova/sentiment140)

- Download the CSV file and place it in the job/ directory.

### Sentiment Keyword

https://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html

[A list of English positive and negative opinion words or sentiment words](http://www.cs.uic.edu/~liub/FBS/opinion-lexicon-English.rar)

- This is a list of approximately 6,800 English positive and negative opinion/sentiment words.
- Download the compressed file, extract the .txt files, and place them in the job/ directory.

### Executing Hadoop cluster

```shell
docker-compose up -d && \
docker exec -it namenode /bin/bash
```

### Upload txt file to HDFS

```shell
# 1. 데이터를 저장할 입력 디렉토리 생성
hdfs dfs -mkdir -p /user/root/sentiment_analysis/input && \
# 2. txt 파일을 HDFS로 업로드
hdfs dfs -put /job/training.1600000.processed.noemoticon.csv /user/root/sentiment_analysis/input && \
# 3. 파일이 정상적으로 업로드되었는지 확인
hdfs dfs -ls /user/root/sentiment_analysis/input 
```

### Run MapReduce Job

```shell
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
    -files /job/mapper.py,/job/reducer.py,/job/positive-words.txt,/job/negative-words.txt \
    -input /user/root/sentiment_analysis/input/training.1600000.processed.noemoticon.csv \
    -output /user/root/sentiment_analysis/output \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py"
```

### Result

```shell
# 1. 결과 폴더 내용 확인
hdfs dfs -ls /user/root/sentiment_analysis/output
```

```shell
# 2. 결과 파일 HDFS 에서 가져오기
hdfs dfs -get /user/root/sentiment_analysis/output/part-00000 ./result.txt
```

```
# 3. 결과 파일 로컬로 가져오기 (로컬 터미널에서 입력)
docker cp namenode:/result.txt ./result.txt
```

<Result.txt>
```
negative	325767
neutral	787384
positive	486849
```