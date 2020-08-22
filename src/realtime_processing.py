from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import *
from pyspark.sql.types import *

if __name__ == '__main__':
    
    spark = SparkSession.builder \
        .appName("test") \
        .getOrCreate()
    
    #sc = spark.sparkContext
    #ssc = StreamingContext(sc, 60)

    brokers = "app-spark_kafka_1:9092,app-spark_kafka_2:9092,app-spark_kafka_3:9092"
    sourceTopic = "sensor-data"
    #sinkTopic = "sensor-data-sink"

    kafkaDataFrame = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", brokers) \
        .option("subscribe", sourceTopic) \
        .load()
    
    stringFormattedDataFrame = kafkaDataFrame.selectExpr("CAST(value AS STRING) as value")
    
    coordSchema = StructType() \
        .add("lat", DoubleType()) \
        .add("lon", DoubleType())

    mainSchema = StructType() \
        .add("temperature", DoubleType()) \
        .add("humidity", DoubleType()) \
        .add("ph", DoubleType()) \
        .add("whc", DoubleType())
    
    schema = StructType() \
        .add("id", LongType()) \
        .add("date", StringType()) \
        .add("coord", coordSchema) \
        .add("main", mainSchema)
    

    jsonParsedDataFrame = stringFormattedDataFrame \
        .select(from_json(stringFormattedDataFrame.value, schema) \
        .alias("sensor_data"))
    formattedDataFrame = jsonParsedDataFrame \
        .select(
            col("sensor_data.id").alias("id"),
            col("sensor_data.date").alias("date"),
            col("sensor_data.coord.lat").alias("lat"),
            col("sensor_data.coord.lon").alias("lon"),
            col("sensor_data.main.temperature").alias("temperature"),
            col("sensor_data.main.humidity").alias("humidity"),
            col("sensor_data.main.ph").alias("ph"),
            col("sensor_data.main.whc").alias("whc")
        )
    query = formattedDataFrame \
        .writeStream \
        .outputMode("append") \
        .format("json") \
        .option("path", "/tmp/output.json") \
        .option("checkpointLocation", "/tmp/state") \
        .start()
    
    query.awaitTermination()