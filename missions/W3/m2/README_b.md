### Running container

```
docker compose up -d
```
```
docker exec -it namenode bash
```

### Running script
- 설정 변경 스크립트(modify_configs.py)

    - Usage: python3 modify_configs.py <config_json_file_path> [hadoop_config_dir_absolute_path]

    - 2번째 인자인 하둡 설정 폴더 절대 경로의 경우 입력하지 않을 시 기본값인 /opt/hadoop/etc/hadoop 으로 설정됨
    - 변경할 설정값들은 updated_config.json에서 확인 가능

- 설정 변경 스크립트(verify_configs.py)

    - Usage: python3 verify_configs.py <config_json_file_path>
    - 수행 작업 목록 

        - 변경된 설정 값 검증

        - test 파일 생성 후 replication factor 확인

        - "yarn node -list -showDetails" 실행

        - hadoop-mapreduce-examples-3.3.6.jar에서 "pi 2 10" 맵리듀스 작업 실행

        

```
cd $HADOOP_HOME/etc/hadoop
```
```
python3 modify_configs.py updated_config.json /opt/hadoop/etc/hadoop
```
```
python3 verify_configs.py updated_config.json
```
