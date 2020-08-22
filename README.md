# How to
## prerequisite(Directory)
```
APP-SPARK
- fluentd/
  - Dockerfile/
    - Dockerfile
  - etc/
    - Configuration File
- kafka/
  - kafka/ (Kafka Binary)
  - kafka-docker/ (clone from https://github.com/wurstmeister/kafka-docker)
- src/
  - spark-code
- docker-compose.yml
```

## Run
- run containers
```
docker-compose up -d
```

- create topics on kafka
```
./kafka/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 3 --topic sensor-data
```

- data into fluentd

```
curl -X POST -d 'json={"id":1851632, "date":"2020-08-22 01:00", "coord": {"lon": 143.19, "lat": 42.92}, "main":{"temperature": 10.6, "humidity": 99, "ph": 5.5, "whc": 64.6}}' http://localhost:9999/sensor.data
```

## PySpark
- create container for spark submit

```
docker run -it --rm -v $(pwd):/data --net app-spark_spark-app ubuntu:latest /bin/bash
```

- execute on container
```
apt update && apt upgrade -y && apt install default-jdk
wget https://ftp.jaist.ac.jp/pub/apache/spark/spark-3.0.0/spark-3.0.0-bin-hadoop3.2.tgz
wget https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
bash Anaconda3-2020.07-Linux-x86_64.sh
tar zfx spark-3.0.0-bin-hadoop3.2.tgz
cd spark-3.0.0-bin-hadoop3.2
export SPARK_HOME=$(pwd)
```

- submit
```
./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 --class org.apache.spark.examples.SparkPi --master spark://SPARK_MASTER_IP:7077 ./data/src/realtime_processing.py 
```

## Reference
- https://www.shuwasystem.co.jp/book/9784798053776.html