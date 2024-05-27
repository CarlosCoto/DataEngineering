from pyspark.sql.types import *
from pyspark.sql.functions import *


def transform_data(input_df):
    transformed_df = (input_df
                      .select("Source_airport") \
                        .groupBy("Source_airport").count() \
                        .orderBy(desc("count")) \
                        .limit(10))
    return transformed_df
