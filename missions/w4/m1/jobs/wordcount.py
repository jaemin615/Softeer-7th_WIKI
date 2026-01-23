from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, lower

spark = SparkSession.builder \
    .appName("WordCountExample") \
    .getOrCreate()

input_path = "/opt/spark/data/sherlock.txt"
text_df = spark.read.text(input_path)


words_df = text_df.select(
    explode(split(col("value"), r"\W+")).alias("word")
).filter(col("word") != "") \
 .select(lower(col("word")).alias("word"))

word_counts = words_df.groupBy("word").count()

output_base = "/opt/spark/data/output"

word_counts.coalesce(1).write.mode("overwrite") \
    .option("header", "true") \
    .csv(f"{output_base}/wordcount_csv")

word_counts.coalesce(1).write.mode("overwrite") \
    .parquet(f"{output_base}/wordcount_parquet")

spark.stop()