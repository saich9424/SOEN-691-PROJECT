import itertools
import math

from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import StringIndexer
from pyspark.sql import Row, SparkSession
from pyspark.sql.functions import regexp_replace
from pyspark.sql.types import IntegerType




def init_spark():
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL basic example") \
        .config("spark.executor.memory", '10g') \
        .config("spark.driver.memory", '10g') \
        .config("spark.memory.offHeap.size", "8g") \
        .config("spark.network.timeout", "3700s") \
        .config("spark.executor.heartbeatInterval", "3600s") \
        .config("spark.storage.blockManagerSlaveTimeoutMs", "3800s") \
        .getOrCreate()
    return spark

spark = init_spark()
restaurant_file_name = "../data/zomato_restaurant.csv"
reviews_file_name = "../data/zomato_reviews.csv"

restaurant_df = spark.read.option("wholeFile", True).option("multiline", True).option("header", True) \
    .option("inferSchema", "True").csv(restaurant_file_name)
restaurant_df = restaurant_df.select(["restaurant_id", "categories", "TotalReviews", "name", "city"])

reviews_df0 = spark.read.option("wholeFile", True).option("multiline", True).option("header", True) \
    .option("inferSchema", "True").csv(reviews_file_name, header=True)
reviews_df0 = reviews_df0.withColumn('user_id', regexp_replace('user_id', '=-', ''))

review_count_per_user = reviews_df0.groupBy('user_id').count()
print('no of users', reviews_df0.select(['user_id']).distinct().count())
# review_count_per_user = review_count_per_user.rdd.filter(lambda x: x[1] > 4).toDF()
reviews_df0 = reviews_df0.join(review_count_per_user, 'user_id', 'leftsemi')

indexer = StringIndexer(inputCol="user_id", outputCol="user_index", handleInvalid='skip')
reviews_df0 = indexer.fit(reviews_df0).transform(reviews_df0)
reviews_df0 = reviews_df0.withColumn("user_index", reviews_df0["user_index"].cast(IntegerType()))
reviews_df0 = reviews_df0.withColumn("user_rating", reviews_df0["user_rating"].cast(IntegerType()))
reviews_df0 = reviews_df0.select(["restaurant_id", "user_index", "user_rating"])
# reviews_df0 = reviews_df0.filter(reviews_df0['user_id'] == "ia1nTRAQEaFWv0cwADeK7g")
print('unique user index', reviews_df0.count())

restaurant_df = restaurant_df.filter(restaurant_df['restaurant_id'] != "#NAME?")
restaurant_df = restaurant_df.filter(restaurant_df.categories.like('%Restaurants%'))
restaurant_df = restaurant_df.filter(restaurant_df['TotalReviews'] > 5)
restaurant_df = restaurant_df.filter(restaurant_df['city'] == "Kolkata")

print('no of records : ', restaurant_df.count())
# restaurant_df.toPandas().to_csv('no_of_records1.csv')

indexer = StringIndexer(inputCol="restaurant_id", outputCol="restaurant_index")
restaurant_df = indexer.fit(restaurant_df).transform(restaurant_df)
restaurant_df = restaurant_df.withColumn("restaurant_index", restaurant_df["restaurant_index"].cast(IntegerType()))
restaurant_df = restaurant_df.select(["restaurant_index", "restaurant_id", "categories"])

temp_restaurant_df = restaurant_df

categories_rdd = restaurant_df.rdd.map(lambda x: x['categories'].split(','))
categories_rdd = categories_rdd.map(lambda x: set(x))
categories_set = categories_rdd.reduce(lambda x, y: x.union(y))


#############################################################################

def add_columns(x):
    temp_dict = x.asDict()
    restaurant_category = [element.lstrip() for element in x.categories.split(',')]
    for element in categories_set:
        temp_dict[element] = 1 if element in restaurant_category else 0
    output = Row(**temp_dict)
    return output


restaurant_rdd = restaurant_df.rdd.map(lambda x: add_columns(x))
restaurant_df = restaurant_rdd.filter(lambda x: sum(x[0:len(x) - 3]) != 0).toDF()
reviews_restaurant_df = reviews_df0.join(restaurant_df, 'restaurant_id')

norm = restaurant_df.rdd.map(lambda x: (x['restaurant_index'], math.sqrt(sum(x[0:len(x) - 3])))).toDF(
    ['restaurant_index', 'norm_value'])
restaurant_reviews_df = restaurant_df.join(reviews_restaurant_df, 'restaurant_index', how='leftsemi')
restaurant_reviews_norm_df = restaurant_reviews_df.join(norm, 'restaurant_index')
restaurant_reviews_norm_df = restaurant_reviews_norm_df.drop('restaurant_id', 'categories')

norm.show(5)
reviews_restaurant_df.show(5)
restaurant_reviews_df.show(5)

temp_norm = restaurant_reviews_norm_df.select(
    ['restaurant_index', 'Afghan;Restaurants', 'Barbeque;Restaurants', 'norm_value'])
print('Norm values')
temp_norm.show(5)


def norm_row(x):
    dict1 = x.asDict()
    norm_value = dict1.pop('norm_value')
    dict1.update((k, v / norm_value) for k, v in dict1.items() if k != 'restaurant_index')
    return Row(**dict1)


norm = restaurant_reviews_norm_df.rdd.map(lambda x: norm_row(x)).toDF()

norm.show(5)

df_dict = restaurant_df.groupBy().sum().collect()[0].asDict()
restaurant_count = restaurant_df.count()

idf_dict = {}

for i in categories_set:
    idf_dict[i] = math.log10(restaurant_count / (df_dict['sum(' + i + ')']))

x = itertools.islice(idf_dict.items(), 0, 5)

for key, value in x:
    print(key, ' : ', value)


(training_data, test_data) = reviews_restaurant_df.randomSplit([0.8, 0.2], seed=123)
reviews_restaurant_tdf = training_data.join(norm, 'restaurant_index')


def update_ratings(x):
    dict1 = x.asDict()
    dict1.update((k, v * (1 if dict1['user_rating'] > 2 else -1))
                 for k, v in dict1.items() if
                 k != 'restaurant_index' and k != 'user_rating' and k != 'user_index')
    return Row(**dict1)


reviews_restaurant_tdf = reviews_restaurant_tdf.rdd.map(lambda x: update_ratings(x)).toDF()
updated_ratings_df = reviews_restaurant_tdf.groupBy('user_index').sum()
updated_ratings_df = updated_ratings_df.drop('sum(user_index)', 'sum(user_rating)', 'sum(restaurant_index)')
updated_ratings_df = updated_ratings_df.rdd.filter(lambda x: sum(x[1:-1]) != 0).toDF()

print('user profile')
updated_ratings_df.show(5)

test_data = test_data.join(updated_ratings_df, 'user_index')
predictions = test_data.join(norm, 'restaurant_index')
predictions.show(5)

def prediction_method(x):
    dict1 = x.asDict()
    score1, score2, ans = 0, 0, 0

    for c in categories_set:
        a = dict1[c]
        b = dict1['sum(' + c + ')']
        score1 = score1 + (a ** 2)
        score2 = score2 + (b ** 2)
        ans = ans + (a * b)

    ans = ans / (math.sqrt(score1) * math.sqrt(score2))
    ans = 1 + 2 * (ans + 1)
    output = {'user_index': dict1.pop('restaurant_index'), 'restaurant_index': dict1.pop('user_index'), 'user_rating': dict1.pop('user_rating'),
              'prediction': ans}
    return Row(**output)


predictions = predictions.rdd.map(lambda x: prediction_method(x)).toDF()
print('Predictions')
predictions.show(5)

evaluator = RegressionEvaluator(metricName='rmse', labelCol='user_rating', predictionCol='prediction')
rmse = evaluator.evaluate(predictions)

print("RMSE : ", rmse)
