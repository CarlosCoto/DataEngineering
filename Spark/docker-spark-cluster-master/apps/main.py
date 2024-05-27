#main module of the solution
#Please mind that, for simplicity, only two functions are defined (init_spark and main), and no UDF are used.
#Also for simplicity and time constrains no error handling (try-catch) implemented for the assessment, __init__ file neither included
#
#awaitTermination is also not included in queries execution

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark import SparkFiles
from pyspark.sql.functions import *
from pyspark.streaming import *
from pyspark.sql.types import *
from pyspark.sql.types import *
from pyspark.sql import Row

def init_spark():
  
  sparkSession = SparkSession.builder\
    .appName("flights-app")\
    .getOrCreate()
  sc = sparkSession.sparkContext
  url = ""
  sc.addFile(url)
  return sparkSession

def main():
  
  spark= init_spark()

  print("Running Flighs-app Spark Session...")

##############################################
#Task 1 : Read csv file and save to filesystem
##############################################

  print("Startint Task 1...")

  print("Reading data from url")

  raw_df = spark.read.option("sep", ",").csv("file:///" + SparkFiles.get("routes.dat"))

  print("Showing raw data")

  raw_df.show(10)

#Delete rows with \N (null) values

  routes_filter_df = raw_df \
                   .filter(raw_df._c0 != "\\N") \
                   .filter(raw_df._c1 != "\\N") \
                   .filter(raw_df._c2 != "\\N") \
                   .filter(raw_df._c3 != "\\N") \
                   .filter(raw_df._c4 != "\\N") \
                   .filter(raw_df._c5 != "\\N") \
                   .filter(raw_df._c6 != "\\N") \
                   .filter(raw_df._c7 != "\\N") \
                   .filter(raw_df._c8 != "\\N") 
                   
  
  df_new=routes_filter_df.withColumnRenamed("_c0","Airline")\
    .withColumnRenamed("_c1","Airline_ID")\
    .withColumnRenamed("_c2","Source_airport")\
    .withColumnRenamed("_c3","Source_airport_ID")\
    .withColumnRenamed("_c4","Destination_airport")\
    .withColumnRenamed("_c5","Destination_airport_ID")\
    .withColumnRenamed("_c6","Codeshare")\
    .withColumnRenamed("_c7","Stops")\
    .withColumnRenamed("_c8","Equipment")
   

  print("Showing column-renamed and cleaned data")

  df_new.show()
 
  df_new.createOrReplaceTempView("flights_information")

  #In spark.sql

  top_airports = spark.sql("""
    SELECT Source_airport, COUNT(Source_airport) as Count 
  FROM flights_information 
  GROUP BY Source_Airport
  ORDER BY Count DESC LIMIT 10
 """)
#dense_rank can be used in the query!

  print("Most frequent airports as source with counts")

  top_airports.show()
  
  #Write to sink
  csvPath = "./output/batch"
  
  top_airports \
  .write \
  .format("csv") \
  .mode("overwrite") \
  .option("header", "true") \
  .save("/app/files")
 

  print("Output .csv file saved in", csvPath)

  ########################################
  #Task 2: Change to structured streaming 
  ########################################

  print("Startint Task 2...")

  #output will be printed in console, same result as batch processing

  checkDirectory = "./apps/output/streaming/check"
  outputDirectory = "./apps/output/streaming/"
  #Define schema required for Structured streaming

  fileSchema = (StructType()
  .add(StructField("Airline", StringType(), True))
  .add(StructField("Airline_ID", IntegerType()))
  .add(StructField("Source_airport", StringType(), True))
  .add(StructField("Source_airport_ID", IntegerType()))
  .add(StructField("Destination_airport", StringType(), True))
  .add(StructField("Destination_airport_ID", IntegerType()))
  .add(StructField("Codeshare", StringType(), True))
  .add(StructField("Stops", IntegerType()))
  .add(StructField("Equipment", StringType(), True))
  )

  inputDF_streaming = (spark
  .readStream
  .schema(fileSchema)
  .option("header", False)
  .option("maxFilesperTrigger ",1)
  .csv(SparkFiles.getRootDirectory())) #stream needs to read from directory

 #cleaning 
      
  transformed_df = inputDF_streaming \
                   .filter(inputDF_streaming.Airline.isNotNull()) \
                   .filter(inputDF_streaming.Airline_ID.isNotNull()) \
                   .filter(inputDF_streaming.Source_airport.isNotNull()) \
                   .filter(inputDF_streaming.Source_airport_ID.isNotNull()) \
                   .filter(inputDF_streaming.Destination_airport.isNotNull()) \
                   .filter(inputDF_streaming.Destination_airport_ID.isNotNull()) \
                   .filter(inputDF_streaming.Codeshare.isNotNull()) \
                   .filter(inputDF_streaming.Stops.isNotNull()) \
                   .filter(inputDF_streaming.Equipment.isNotNull())
      
  print("Showing transformed dataframe")

  transformed_df.writeStream \
    .trigger(processingTime="10 minutes") \
    .format("console") \
    .outputMode("update") \
    .start()


  transformed_df.printSchema()

  spark.conf.set("spark.sql.shuffle.partitions", 200)

# Select the source airport column and count the occurrences


  streaming_top_airports = transformed_df \
                        .select("Source_airport") \
                        .groupBy("Source_airport").count() \
                        .orderBy(desc("count")) \
                        .limit(10)


  
  streaming_top_airports.printSchema()


  print("Streaming DataFrame : " + str(streaming_top_airports.isStreaming))

# Write the streaming output to the console

  print("Top Source Airports with structured streaming ouput")

  streamingQuery = streaming_top_airports \
    .writeStream \
    .format("console") \
    .outputMode("complete") \
    .trigger(processingTime="10 minutes") \
    .start()
    

#############################
#Task 3: Use sliding windows
#############################

#including dummy timestamp
 
  transformed_df_withEvents = transformed_df \
     .selectExpr(
    "*",
    "cast(cast(Destination_airport_ID as double)/1000000 as timestamp) as dummy_event_time"
  )

#Create window (more pseudocode..)

  transformed_df_withEvents = transformed_df_withEvents \
                              .filter((transformed_df_withEvents.dummy_event_time.isNotNull()))

  windows_df = transformed_df_withEvents \
    .groupBy(window(col("dummy_event_time"), "10 minutes", "5 minutes"), col("Source_airport"))\
    .count() \
    .orderBy(desc("count")) \
    .limit(10)

  windows_df.printSchema()


  windows_df \
    .writeStream \
    .format("console") \
    .outputMode("complete") \
    .trigger(processingTime="10 minutes") \
    .start().awaitTermination()
  
#Here we could call the testing module test_main.py!


  print("Closing spark session...")

  spark.stop()

  print("Spark session ended")

  print("End of program...")
  
  
if __name__ == '__main__':
  main()