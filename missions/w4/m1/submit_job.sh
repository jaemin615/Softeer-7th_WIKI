#!/bin/bash

docker exec spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --name "Pi_Estimation_Job" \
  /opt/spark/examples/src/main/python/pi.py 10