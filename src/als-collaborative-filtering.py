import os
import sys

from pyspark.ml.feature import StringIndexer
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.rdd import RDD
from pyspark.sql import Row
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, regexp_replace
from pyspark.sql.functions import desc
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
import pandas as pd
from pyspark.sql.functions import col, avg
from pyspark.sql.types import IntegerType


def init_spark():
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL basic example") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()
    return spark

spark = init_spark()
sc = spark.sparkContext
restaurant_file_name = "../data/zomato_restaurant.csv"
reviews_file_name = "../data/zomato_reviews.csv"

restaurant_df = spark.read.option("wholeFile", True).option("multiline", True).option("header", True)\
    .option("inferSchema", "True").csv(restaurant_file_name)
restaurant_df = restaurant_df.filter(restaurant_df['business_id'] != "#NAME?")


reviews_df = spark.read.option("wholeFile", True).option("multiline", True).option("header", True)\
    .option("inferSchema","True").csv(reviews_file_name, header=True)
reviews_df = reviews_df.withColumn('user_id', regexp_replace('user_id', '=-', ''))

restaurant_df = restaurant_df.filter(restaurant_df['city'] == "Phoenix")
restaurant_df = restaurant_df.select(["business_id", "categories", "review_count", "name", "city"])

indexer = StringIndexer(inputCol="business_id", outputCol="business_index")
restaurant_df = indexer.fit(restaurant_df).transform(restaurant_df)
restaurant_df = restaurant_df.withColumn("business_index", restaurant_df["business_index"].cast(IntegerType()))


reviews_df = reviews_df.select(["business_id", "user_id", "stars"])

restaurant_reviews_df = reviews_df.join(restaurant_df, ['business_id'])
restaurant_reviews_df = restaurant_reviews_df.filter(restaurant_reviews_df.business_id.isNotNull())
restaurant_reviews_df = restaurant_reviews_df.filter(restaurant_reviews_df.user_id.isNotNull())

indexer = StringIndexer(inputCol="user_id", outputCol="user_index")
restaurant_reviews_df = indexer.fit(restaurant_reviews_df).transform(restaurant_reviews_df)
restaurant_reviews_df = restaurant_reviews_df.withColumn("user_index", restaurant_reviews_df["user_index"].cast(IntegerType()))

restaurant_reviews_city_df = restaurant_reviews_df.select(["business_index", "user_index", "business_id", "user_id", "stars"])
print(restaurant_reviews_city_df.first())

restaurant_reviews_city_df = restaurant_reviews_city_df.withColumn("stars", restaurant_reviews_city_df["stars"].cast(IntegerType()))

restaurant_reviews_city_df.toPandas().to_csv('mycsv.csv')



(training, test) = restaurant_reviews_city_df.randomSplit([0.8, 0.2], 123)

# als = ALS(maxIter=20, regParam=0.01, userCol="user_index", itemCol="business_index", ratingCol="stars",
#           coldStartStrategy="drop", rank=70).setSeed(123)
# model = als.fit(training)
# predictions = model.transform(test)
# # predictions.cache()
#
# evaluator = RegressionEvaluator(metricName="rmse", labelCol="stars", predictionCol="prediction")
# rmse = evaluator.evaluate(predictions)
# print(rmse)

als = ALS(userCol="user_index", itemCol="business_index", ratingCol="stars", coldStartStrategy="drop")
als.setSeed(123)
grid = ParamGridBuilder().addGrid(als.maxIter, [20]).addGrid(als.rank, [20,30,40,50,60,70]).addGrid(als.regParam, [0.45,0.5,0.55]).build()
evaluator = RegressionEvaluator(predictionCol=als.getPredictionCol(),labelCol=als.getRatingCol(), metricName='rmse')
cv = CrossValidator(estimator=als, estimatorParamMaps=grid, evaluator=evaluator, numFolds=5)
cvModel = cv.fit(training)

predictions = cvModel.transform(test)
predictions.cache()

print('########################## Computing RMSE ###########################')

rmse_evaluator = RegressionEvaluator(predictionCol='prediction',labelCol='stars', metricName='rmse')
rmse = rmse_evaluator.evaluate(predictions)
print(rmse)
