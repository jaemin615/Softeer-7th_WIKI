### Setting up volume directories for Docker containers
```bash
mkdir -p data logs spark-events notebooks
```

### Build docker image
```bash
docker-compose up -d
```
### Spark master web UI
http://localhost:8080/
### Spark worker1 web UI
http://localhost:8081/
### Spark worker2 web UI
http://localhost:8082/
### Spark history-server web UI
http://localhost:18080/


### Jupyterlab
http://localhost:8888/

open m2.ipynb in http://localhost:8888/

