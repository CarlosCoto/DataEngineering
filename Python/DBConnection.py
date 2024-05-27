# See instructions for installing Requests module for Python
# https://requests.readthedocs.io/en/master/user/install/#install

import pandas as pd
import numpy as np
import requests
import json
import psycopg2
#from sqlalchemy import create_engine
#import urllib.request
from urllib.parse import quote_plus

#engine = create_engine('postgresql://postgres:%s@localhost/postgres' % quote_plus(''))

try:
      connection = psycopg2.connect(database='postgres',
                        host='localhost',
                        user='postgres',
                        password='', #needs to be secured
                        port='5432')
      cursor = connection.cursor()

      #create table in DB (if not exist)
      #sql_query = "CREATE TABLE IF NOT EXISTS public.\"sessions\" (session_id INTEGER PRIMARY KEY,event_customer_id INTEGER NOT NULL,event_timestamp TIMESTAMP NOT NULL,type TEXT NOT NULL, time_delta TIMESTAMP NOT NULL, session_start BOOLEAN NOT NULL);"

      #sql_query = "CREATE TABLE IF NOT EXISTS public.\"test\" (id bigint) TABLESPACE pg_default; ALTER TABLE IF EXISTS public.\"test\" OWNER to postgres;"
      
      sql_query = (
        """
        CREATE TABLE test (
            test_id SERIAL PRIMARY KEY,
            test_name VARCHAR(255) NOT NULL
        )
        """)
      
      cursor.execute(sql_query)
      cursor.close()
      connection.commit()

      #db_version = cursor.fetchone()
      #print(db_version)
      #df_session.to_sql('sessions', engine, if_exists='replace')
except (Exception, psycopg2.DatabaseError) as error:
        print(error)
finally:
        if connection is not None:
            connection.close()