import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import substring_index, when, count, concat, col, lit
from pyspark.sql.types import *

import time

start_time = time.time()
output_dir = sys.argv[1]

spark = SparkSession.builder.appName("telecom").master("local").config("spark.sql.warehouse.dir", "file:///C:/warehouse/").getOrCreate()

gsm_file_location = 'gsm.csv'
umts_file_location = 'umts.csv'
lte_file_location = 'lte.csv'
site_file_location = 'site.csv'

cells_df_src = spark.read.format("csv") \
    .option("inferSchema", "true") \
    .option("header", "true") \
    .option("sep", ";") \
    .load([gsm_file_location, umts_file_location, lte_file_location])

print("Source file schema:")
cells_df_src.printSchema()

cells_df_tmp = cells_df_src.withColumn("g", substring_index(F.reverse(F.split(F.input_file_name(), "/")).getItem(0), ".", 1))

cells_df_tmp.write.option("header", True) \
    .partitionBy("year", "month", "day") \
    .mode("overwrite") \
    .csv("file:///" + output_dir)

schema = StructType(
    [StructField('year', IntegerType(), True),
     StructField('month', IntegerType(), True),
     StructField('day', IntegerType(), True),
     StructField('cell_identity', StringType(), True),
     StructField('frequency_band', IntegerType(), True),
     StructField('site_id', IntegerType(), True),
     StructField("g", StringType(), True)
     ]
)

cells_df_partitioned = spark.read.format("csv") \
    .option("header", "true") \
    .option("sep", ",") \
    .schema(schema) \
    .load(output_dir)

print("Data from hdfs:")
cells_df_partitioned.show(truncate=False)

cells_df = cells_df_partitioned.withColumn("site_id", concat(lit("site_"), col("site_id"))) \
    .withColumn("frequency_band", concat(col("frequency_band"), lit(" MHZ"))) \
    .withColumn("technology", when(cells_df_partitioned.g == "gsm", "2g")
                .when(cells_df_partitioned.g == "umts", "3g")
                .when(cells_df_partitioned.g == "lte", "4g")
                .otherwise("unknown"))

print("Transformed data:")
cells_df.show(truncate=False)

print("Aggregated data:")
cells_df.groupBy("technology", "site_id")\
    .agg(count("*").alias("count"))\
    .orderBy("technology", "site_id")\
    .show(truncate=False)

print("Cells per technology on each site:")
cells_df.groupBy("technology") \
    .pivot("site_id") \
    .agg(count("*").alias("count")) \
    .na.fill(value=0) \
    .show(truncate=False)

print("Number of cells per frequency band on a particular site")
cells_df.groupBy("technology", "site_id", "frequency_band") \
    .agg(count("*").alias("count")) \
    .orderBy("technology", "site_id", "frequency_band") \
    .show(truncate=False)

# site_df = spark.read.format("csv") \
#     .option("inferSchema", "true") \
#     .option("header", "true") \
#     .option("sep", ";") \
#     .load(site_file_location)
#
# site_df.show(20, False)

# new_df = cells_df.join(site_df, cells_df['site_id'] == site_df['site_id'], 'left_outer').drop(cells_df['site_id'])

# new_df.groupBy("site_id", "cell_identity").count().show()
print(f"Execution time: {time.time() - start_time} seconds")
