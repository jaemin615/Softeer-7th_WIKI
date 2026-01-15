### Download data file

Using the Software Category Review Data in the Amazon 2023 Review Dataset

```shell
curl --create-dirs -o ./data/Software.jsonl.gz https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/Software.jsonl.gz
gunzip ./data/Software.jsonl.gz
```

### Executing Hadoop cluster

```shell
docker-compose up -d
```

### Upload data file to HDFS

```shell
docker cp mapper.py namenode:/     && \
docker cp reducer.py namenode:/    && \
docker cp ./data/Software.jsonl  namenode:/
```

```shell
docker exec -it namenode hdfs dfs -mkdir -p /user/root/amazon/input && \
docker exec -it namenode hdfs dfs -put Software.jsonl /user/root/amazon/input 
```

### Run MapReduce Job

```shell
docker exec -it namenode hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
    -files /mapper.py,/reducer.py \
    -input /user/root/amazon/input/Software.jsonl \
    -output /user/root/amazon/output \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py"
```

### Get Result

```shell
docker exec -it namenode hdfs dfs -get /user/root/amazon/output/part-00000 ./result.txt && \
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
1. Total Unique ASINs: 90359

2. Top 10 Data (Ordered by Number of Reviews):
-----------------------------------------------
ASIN           Count    AvgRating
B00FAPF5U0      50891    4.3       
B00N28818A      46940    3.8       
B00992CF6W      44324    4.4       
B005ZXWMUS      33079    4.2       
B0094BB4TW      30212    3.3       
B00KDSGIPK      27666    4.0       
B01N0BP507      27101    4.4       
B00QW8TYWO      26870    4.6       
B017250D16      26026    2.7       
B07T771SPH      25099    4.4       

3. Top 10 Data (Ordered by Rating):
-----------------------------------------------
ASIN           Count    AvgRating
B0C3Z6XS3L      2        5.0       
B0C39R1GZR      1        5.0       
B0C2J7MB9G      1        5.0       
B0C2J7CMZC      1        5.0       
B0BZFGX5R1      1        5.0       
B0BZ2K72LD      1        5.0       
B0BYSLHXMV      7        5.0       
B0BY3LVJZ7      1        5.0       
B0BXPL1QK2      2        5.0       
B0BX88HS2S      1        5.0       

===============================================
        [STEP 1] RAW DATA VERIFICATION         
===============================================
Target ASIN  : B00CTQ6SIG
Raw Count    : 10256
Raw Avg Rate : 4.2735

-----------------------------------------------
       [STEP 2] MAPREDUCE RESULT CHECK 
-----------------------------------------------
Target ASIN  : B00CTQ6SIG
MR Count     : 10256
MR Avg Rate  : 4.3
(Note: Rounded to the first decimal place)

>> [SUCCESS] Review Counts match!
===============================================
```