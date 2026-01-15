### Project Structure
```
. 
├── configs/ 
├── wordcount/
│	└── mapper.py 
│	└── reducer.py 
│   └── sherlock.txt 
├── Dockerfile
├──  docker-compose.yml 
└── start_hadoop.sh 
```
### Ebook
[The Adventures of Sherlock Holmes](https://www.gutenberg.org/cache/epub/1661/pg1661.txt)

### Download txt file

```bash
curl https://www.gutenberg.org/cache/epub/1661/pg1661.txt -o ./wordcount/sherlock.txt
```

### Executing Hadoop cluster

```shell
docker-compose up -d && \
docker exec -it namenode /bin/bash
```

### Upload txt file to HDFS

```shell
# 1. 데이터를 저장할 입력 디렉토리 생성
hdfs dfs -mkdir -p /user/root/wordcount/input && \
# 2. txt 파일을 HDFS로 업로드
hdfs dfs -put /wordcount/sherlock.txt /user/root/wordcount/input/ && \
# 3. 파일이 정상적으로 업로드되었는지 확인
hdfs dfs -ls /user/root/wordcount/input/ 
```

### Run MapReduce Job

```shell
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar\
	-files /wordcount/mapper.py,/wordcount/reducer.py \
	-input /user/root/wordcount/input/sherlock.txt \
	-output /user/root/wordcount/output \
	-mapper "python3 mapper.py" \
	-reducer "python3 reducer.py"
```

### Result

```shell
# 1. 결과 폴더 내용 확인
hdfs dfs -ls /user/root/wordcount/output
```

```shell
# 2. 결과 파일 HDFS 에서 가져오기
hdfs dfs -get /user/root/wordcount/output/part-00000 ./wordcount_result.txt
```

```
# 3. 결과 파일 로컬로 가져오기 (로컬 터미널에서 입력)
docker cp namenode:/wordcount_result.txt ./wordcount_result.txt
```

### Analysis

```shell
# 가장 빈도 수 높은 단어 20개
cat wordcount_result.txt | sort -k2 -nr | head -n 20
```

```text
the	5809
and	3082
i	3038
to	2825
of	2772
a	2701
in	1824
that	1767
it	1746
you	1573
he	1486
was	1412
his	1159
is	1146
my	1007
have	930
with	875
as	863
had	831
at	780
```

```shell
# 원본 파일에서 해당 단어의 총 빈도수 계산
 grep -oi "watson" wordcount/sherlock.txt | wc -l
```

81


```shell
# 결과 파일에서 해당 단어 찾기
grep -w "watson" wordcount_result.txt
```

watson	81
