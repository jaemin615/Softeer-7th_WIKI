#!/bin/bash

# 네임노드 디렉토리가 비어있으면 포맷 진행
if [ ! -d "/opt/hadoop/data/name/current" ]; then
  echo "Formatting NameNode..."
  $HADOOP_HOME/bin/hdfs namenode -format
fi

# SSH 서비스 시작 (Hadoop 노드 간 통신용)
service ssh start

# Hadoop 서비스 시작
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

tail -F $HADOOP_HOME/logs/*
