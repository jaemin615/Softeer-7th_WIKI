### Docker-compose.yml
도커 파일은 m1의 하둡 도커파일 수정하여 활용
마스터 노드 1개와 워커 노드 2개 설정 / 볼륨 및 네트워크 설정을 진행함

### config files
core-site.xml, hdfs-site.xml, mapred-site.xml, yarn-site.xml -> 공식 문서 참조 설정

workers -> hadoop_worker1, hadoop_worker2 추가
hadoop-env.sh -> JAVA_HOME 명시

### Running Container & MapReduce Operation
모든 컨테이너 실행 후 하둡 맵리듀스 예제 파일로 grep 실행 -> 결과 확인



```
# docker-compose up -d
# docker exec -it hadoop-master bash
```

localhost:9870, localhost:8088 실행하여 상태 확인 가능 
```
# hdfs dfs -mkdir -p /user/test/input
# hdfs dfs -put etc/hadoop/*.xml /user/test/input
# hadoop jar /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar grep /user/test/input /user/test/output 'dfs[a-z.]+'
# hdfs dfs -ls /user/test/output
```



Found 2 items

-rw-r--r--   2 root supergroup          0 2026-01-13 02:43 /user/test/output/_SUCCES

-rw-r--r--   2 root supergroup         77 2026-01-13 02:43 /user/test/output/part-r-00000

```
# hdfs dfs -cat /user/test/output/part-r-00000
```

1       dfsadmin

1       dfs.replication

1       dfs.namenode.name.dir

1       dfs.datanode.data.dir
```
# hdfs dfs -get /user/test/output/part-r-00000 /tmp/result.txt
# cat /tmp/result.txt
```

1       dfsadmin

1       dfs.replication

1       dfs.namenode.name.dir

1       dfs.datanode.data.dir

