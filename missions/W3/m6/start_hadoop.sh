#!/bin/bash

service ssh start

if [ "$NODE_TYPE" == "master" ]; then
  if [ ! -d "/hadoop/dfs/name/current" ]; then
    $HADOOP_HOME/bin/hdfs namenode -format
  fi
  $HADOOP_HOME/sbin/start-dfs.sh
  $HADOOP_HOME/sbin/start-yarn.sh
fi

tail -f /dev/null
