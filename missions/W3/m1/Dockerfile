FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
  openjdk-8-jdk \
  ssh \
  curl \
  vim \
  && apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

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

COPY configs/*.xml $HADOOP_HOME/etc/hadoop/
COPY start_hadoop.sh /start_hadoop.sh
RUN chmod +x /start_hadoop.sh

RUN echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN echo "export HDFS_NAMENODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
  echo "export HDFS_DATANODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
  echo "export HDFS_SECONDARYNAMENODE_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
  echo "export YARN_RESOURCEMANAGER_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh && \
  echo "export YARN_NODEMANAGER_USER=root" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# (HDFS Web UI: 9870, NameNode: 9000, YARN UI: 8088)
EXPOSE 9870 9000 8088

ENTRYPOINT ["/bin/bash", "/start_hadoop.sh"]
