#!/bin/bash

if [ -f "${SPARK_HOME}/bin/load-spark-env.sh" ]; then
    source "${SPARK_HOME}/bin/load-spark-env.sh"
fi

if [ "$SPARK_MODE" == "master" ]; then
    $SPARK_HOME/sbin/start-master.sh 
elif [ "$SPARK_MODE" == "worker" ]; then
    $SPARK_HOME/sbin/start-worker.sh "spark://${SPARK_MASTER_HOST}:${SPARK_MASTER_PORT}"
elif [ "$SPARK_MODE" == "history" ]; then
    $SPARK_HOME/sbin/start-history-server.sh
fi