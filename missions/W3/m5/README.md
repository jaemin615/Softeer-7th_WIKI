
### Download data file

```shell
curl -o ./data.zip https://files.grouplens.org/datasets/movielens/ml-20m.zip
unzip data.zip
```

### Executing Hadoop cluster

```shell
docker-compose up -d
```

### Upload data file to HDFS

```shell
docker cp mapper.py namenode:/     && \
docker cp reducer.py namenode:/    && \
docker cp ./data/ratings.csv  namenode:/
```

```shell
docker exec -it namenode hdfs dfs -mkdir -p /user/root/movie/input && \
docker exec -it namenode hdfs dfs -put ratings.csv /user/root/movie/input 
```

### Run MapReduce Job

```shell
docker exec -it namenode hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
    -files /mapper.py,/reducer.py \
    -input /user/root/movie/input/ratings.csv \
    -output /user/root/movie/output \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py"
```

### Get Result

```shell
docker exec -it namenode hdfs dfs -get /user/root/movie/output/part-00000 ./result.txt && \
docker cp namenode:/result.txt ./result.txt
```

### Verify

```shell
./analyze.sh
```

```text
===============================================
         HADOOP MAPREDUCE REPORT               
===============================================
1. Total Line Count: 26744

2. Top 10 Data (Ordered by ID):
-----------------------------------------------
1	3.9
2	3.2
3	3.2
4	2.9
5	3.1
6	3.8
7	3.4
8	3.1
9	3.0
10	3.4

3. Top 10 Data (Ordered by Rating - DESC):
-----------------------------------------------
99450	5.0
99243	5.0
98761	5.0
95979	5.0
95977	5.0
95517	5.0
94972	5.0
94949	5.0
94737	5.0
94657	5.0

===============================================
   [STEP 1] RAW DATA VERIFICATION (ID: 1)      
===============================================
Target: MovieID 1
Result: Average Rating is 3.9212

-----------------------------------------------
   [STEP 2] MAPREDUCE RESULT CHECK (ID: 1)     
-----------------------------------------------
MapReduce Result for ID 1: 3.9
(Note: Rounded to the first decimal place)
===============================================
```