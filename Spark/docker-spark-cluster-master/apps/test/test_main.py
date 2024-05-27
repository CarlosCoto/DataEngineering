#Test module for showing logic behind
#using unittest, own test class created extending unittest.TestCase
#for simplicity, only included for batch processing
#these methods can be called in main.py or automated (i.e. Azure DevOps)

#It is needed
#input data frame that mimics our source data
#expected data frame which is the output that we expect
#Apply our transformation to the input data frame
#Assert the output of the transformation to the expected data frame

import unittest
from test_classes import SparkETLTestCase
from etl import transform_data
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime
from pyspark.sql import SparkSession


def test_main(self):
    

    #1. Prepare an input data frame that mimics our source data.
    input_schema = StructType([
            StructField('Source_airport', StringType(), True),
            StructField('Count', IntegerType(), True)
            
        ])
    
    #Here we could call the df result of the operations (transformations)

    dummy_input_data = [("ATL",633),
                ("ORD",277),
                ("LAX",209),
                ("LHR",202),
                ("VIE",159),
                ("CDG",155),
                ("FRA",150),
                ("AMS",145),
                ("DFW",143),
                ("DEN",136)
                ]
    
    #using data from out batch job, which will make no sense in prod
    
    input_df = SparkETLTestCase.spark.createDataFrame(data=dummy_input_data, schema=input_schema)


    #2. Prepare an expected data frame which is the output that we expect.        
    expected_schema = StructType([
            StructField('Source_airport', StringType(), True),
            StructField('Count', IntegerType(), True)
            ])
    

    expected_data = [("ATL",633),
                ("ORD",277),
                ("LAX",209),
                ("LHR",202),
                ("VIE",159),
                ("CDG",155),
                ("FRA",150),
                ("AMS",145),
                ("DFW",143),
                ("DEN",136)
                ]
    

    expected_df = self.spark.createDataFrame(data=expected_data, schema=expected_schema)

    #3. Apply our transformation to the input data frame

    transformed_df = transform_data(input_df)

    #4. Assert the output of the transformation to the expected data frame.

    field_list = lambda fields: (fields.name, fields.dataType, fields.nullable)
    fields1 = [*map(field_list, transformed_df.schema.fields)]
    fields2 = [*map(field_list, expected_df.schema.fields)]

    # Compare schema of transformed_df and expected_df

    res = set(fields1) == set(fields2)

    # assert

    (self.assertTrue(res))

    # Compare data in transformed_df and expected_df 
    self.assertEqual(sorted(expected_df.collect()), sorted(transformed_df.collect()))

  #Could print output here
  
if __name__ == '__test_main__':
    test_main()

