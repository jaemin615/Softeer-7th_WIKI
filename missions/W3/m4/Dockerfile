FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
  openjdk-8-jdk \
  openssh-server \
  openssh-client \
  curl \
  vim \
  python3 \
  && apt-get clean

ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
ENV HDFS_NAMENODE_USER=root
ENV HDFS_DATANODE_USER=root
ENV HDFS_SECONDARYNAMENODE_USER=root
ENV YARN_RESOURCEMANAGER_USER=root
ENV YARN_NODEMANAGER_USER=root

RUN curl -O \
  https://ftp.kaist.ac.kr/apache/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz \
  && tar -xvzf hadoop-$HADOOP_VERSION.tar.gz \
  && mv hadoop-$HADOOP_VERSION $HADOOP_HOME \
  && rm hadoop-$HADOOP_VERSION.tar.gz

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa \
  && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys \
  && chmod 0600 ~/.ssh/authorized_keys
RUN echo "Host *" > /etc/ssh/ssh_config.d/ignore-host-key.conf \
  && echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.d/ignore-host-key.conf \
  && echo "    UserKnownHostsFile=/dev/null" >> /etc/ssh/ssh_config.d/ignore-host-key.conf

RUN echo "log4j.logger.org.apache.hadoop.util.NativeCodeLoader=ERROR" >> $HADOOP_HOME/etc/hadoop/log4j.properties

COPY configs/* $HADOOP_HOME/etc/hadoop/
COPY start_hadoop.sh /start_hadoop.sh
RUN chmod +x /start_hadoop.sh

COPY job/*  /job/

# (HDFS Web UI: 9870 YARN UI: 8088)
EXPOSE 9870 8088

ENTRYPOINT ["/bin/bash", "/start_hadoop.sh"]
