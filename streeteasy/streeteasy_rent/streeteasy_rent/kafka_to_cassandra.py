from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import *
from pyspark.sql.functions import *
from pyspark.sql import DataFrame
from pyspark.sql.types import IntegerType
import logging

KEYSPACE = 'test'

def jdbc_batch(table: str, username: str, password: str):
      logging.info(f"Writing to table: {table}")
      def process_batch(df: DataFrame, epoch_id):
            (df.write.format('org.apache.spark.sql.cassandra')
                  .mode('append')
                  .options(table=table, keyspace=KEYSPACE).save())
      
      return process_batch

def main():
      spark: SparkSession = SparkSession.builder.appName('kafka_to_cassandra').getOrCreate()
      df = (spark
            .readStream
            .format('kafka')
            .option('kafka.bootstrap.servers', 'localhost:9092')
            .option('subscribe', 'streeteasy_rent')
            .load())

      streateasy_rent_schema = open('/mnt/e/code/real-estate-dashboard/streeteasy/streeteasy_rent/streeteasy_rent/services/streeteasy_rent.avsc', 'r').read()

      exploded_avro = df\
            .select(
                  from_avro('value', streateasy_rent_schema).alias('data'), 
                  'timestamp')
      
      avro_df = exploded_avro\
            .select(
                  'data.*', 
                  to_timestamp('timestamp').alias('timestamp'))\
            .withColumn(
                  'rent_id', 
                  expr("uuid()"))\
            .withColumn(
                  'price', 
                  regexp_replace(col('price'), "[^\\d]", "").cast(IntegerType()))\
            .withColumn(
                  "days_on_market",
                  when(col("days_on_market") == "Listed Today", 0)
                  .otherwise(regexp_extract(col("days_on_market"), r"(\d+)", 1).cast("int")))
      
      rent_by_neighbourhood_df = avro_df\
                                        .withColumn("neighbourhood", explode('neighbourhood'))\
                                        .drop('amenities')
      amenities_by_rent_df = avro_df\
                                    .withColumn("amenity_title", explode('amenities'))\
                                    .drop('amenities')\
                                    .drop('neighbourhood')
      rent_df = avro_df\
            .drop('amenities')\
            .drop('neighbourhood')
            
      # TODO: These are not used. Create a Connector config to use these
      credentials = {'username': 'cassandra', 'password': 'cassandra'}   
      
      rent_by_neighbourhood_stream = rent_by_neighbourhood_df\
            .writeStream\
            .foreachBatch(jdbc_batch('rent_by_neighbourhood', **credentials))\
            .start()
            
      amenities_by_rent_stream = amenities_by_rent_df\
            .writeStream\
            .foreachBatch(jdbc_batch('amenities_by_rent', **credentials) )\
            .start()
            
      rent_stream = rent_df\
            .writeStream\
            .foreachBatch(jdbc_batch('rent', **credentials))\
            .start()
            
      rent_by_neighbourhood_stream.awaitTermination()
      amenities_by_rent_stream.awaitTermination()
      rent_stream.awaitTermination()
      
      
if __name__ == '__main__':
      main()
      
