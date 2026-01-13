### Dockerfile

```dockerfile
FROM ubuntu:22.04

# 기본 패키지 및 Java 설치
RUN apt-get update && apt-get install -y \
  openjdk-8-jdk \
  ssh \
  curl \
  vim \
  && apt-get clean

# 환경 변수 설정
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Hadoop 다운로드 및 압축 해제
RUN curl -O https://ftp.kaist.ac.kr/apache/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz \
  && tar -xvzf hadoop-$HADOOP_VERSION.tar.gz \
  && mv hadoop-$HADOOP_VERSION $HADOOP_HOME \
  && rm hadoop-$HADOOP_VERSION.tar.gz


# SSH 설정 (비밀번호 없이 접속 가능하도록)
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa \
  && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys \
  && chmod 0600 ~/.ssh/authorized_keys

# SSH 설정 (처음 서버 접속 시 보안 검사 넘어가기 )
RUN echo "Host *" > /etc/ssh/ssh_config.d/ignore-host-key.conf \
  && echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.d/ignore-host-key.conf \
  && echo "    UserKnownHostsFile=/dev/null" >> /etc/ssh/ssh_config.d/ignore-host-key.conf

# Hadoop 설정 파일 복사
COPY configs/*.xml $HADOOP_HOME/etc/hadoop/
COPY start_hadoop.sh /start_hadoop.sh

# Hadoop 실행을 위한 환경 설정 (hadoop-env.sh)
RUN echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Hadoop root 계정 실행 허용 설정 추가
RUN echo "export HDFS_NAMENODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
  echo "export HDFS_DATANODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
  echo "export HDFS_SECONDARYNAMENODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
  echo "export YARN_RESOURCEMANAGER_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
  echo "export YARN_NODEMANAGER_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh


# 포트 노출 (HDFS Web UI: 9870, NameNode: 9000, YARN UI: 8088)
EXPOSE 9870 9000 8088

ENTRYPOINT ["/bin/bash", "/start_hadoop.sh"]
```


### config files

https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html 

공식 문서 참조하여 작성
- core-site.xml
- hdfs-site.xml
- mapred-site.xml
- yarn-site.xml

### start_hadoop.sh

```shell
#!/bin/bash

# NameNode 디렉토리가 비어있으면 포맷 진행
if [ ! -d "/opt/hadoop/data/name/current" ]; then
  echo "Formatting NameNode..."
  $HADOOP_HOME/bin/hdfs namenode -format
fi

# SSH 서비스 시작
service ssh start

# Hadoop 서비스 시작
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

tail -F $HADOOP_HOME/logs/*
```
### Running Container

```
docker build -t hadoop-image .

# 볼륨으로 사용할 로컬 디렉토리 생성 
mkdir ./hadoop_data

# 컨테이너 실행
docker run -d \
  --name hadoop-container \
  -p 9870:9870 \
  -p 8088:8088 \
  -v ./hadoop_data:/opt/hadoop/data \
 hadoop-image 
```

### Data Operations

```
docker exec -it hadoop-container bash

# HDFS 디렉토리 생성
hdfs dfs -mkdir -p /user/test

# 로컬 테스트 파일 생성 및 업로드
echo "Hello World" > hello.txt
hdfs dfs -put hello.txt /user/test/

# 파일 업로드 확인 및 내용 출력
hdfs dfs -ls /user/test/
hdfs dfs -cat /user/test/hello.txt

# 파일 로컬로 다시 복사
hdfs dfs -get /user/test/hello.txt hello_restored.txt
```
