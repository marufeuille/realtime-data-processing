# How to
## prerequisite(Directory)
```
REALTIME-DATA-PROCESSING
- fluentd/
  - Dockerfile/
    - Dockerfile
  - etc/
    - Configuration File
- kafka/
  - kafka-docker/ (clone from https://github.com/wurstmeister/kafka-docker)
- src/
  - spark-code
- work-container
  - Dockerfile for work container
- docker-compose.yml
```

## deploy containers
```
docker-compose up -d
```

## into work container
```
docker exec -it realtime-data-processing_work_1 /bin/bash
```

## create topics on kafka
- in work container
```
kafka-topics.sh --create --zookeeper realtime-data-processing_zookeeper_1:2181 --replication-factor 1 --partitions 3 --topic TOPIC_NAME
```

## send data to kafka via fluentd(http)
- in work container
```
curl -X POST -d 'json={"id":1851632, "date":"2020-08-22 01:00", "coord": {"lon": 143.19, "lat": 42.92}, "main":{"temperature": 10.6, "humidity": 99, "ph": 5.5, "whc": 64.6}}' http://realtime-data-processing_fluentd_1:9999/sensor.data
```

## spark-submit
- get container ip address
```
$ docker inspect realtime-data-processing_spark_1 | jq -c .[0].NetworkSettings.Networks'["realtime-data-processing_realtime-data-nw"]'.IPAddress
"172.20.0.4"
```

- in work container
- submit job
```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 --class org.apache.spark.examples.SparkPi --master spark://172.20.0.4:7077 /data/src/realtime_processing.py
```

## Reference
- https://www.shuwasystem.co.jp/book/9784798053776.html