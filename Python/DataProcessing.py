# See instructions for installing Requests module for Python
# https://requests.readthedocs.io/en/master/user/install/#install

import pandas as pd
import numpy as np
import requests
import json
import psycopg2
from sqlalchemy import create_engine

def execute():

  #requestUrl = "https://storage.googleapis.com/xcc-de-assessment/events.json"

  with open (r"C:", "r") as f:

  #response = requests.get(requestUrl)

    data = [json.loads(line) for line in f]

# Use json_normalize() to create a DataFrame

    df = pd.json_normalize(data, sep='_')

#filter on not-null customer-ids

    df = df[df['event_customer-id'].notnull()]

#convert timestamp to datetime format

  df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])

  df = df.sort_values('event_timestamp')

#create session dataframe copying desired columns

  df_session = df[['event_customer-id', 'event_timestamp', 'type']].copy()

#calculate time delta for each customer_id session

  df_session['time_delta'] = (df_session.groupby('event_customer-id')['event_timestamp']
                      .diff().fillna(pd.Timedelta(seconds=0)))


# Identify session start events (delta greater than 30 minutes)
  df_session['session_start'] = (df_session['time_delta'] > pd.Timedelta(minutes=30))

# Calculate session IDs using cumsum of session_start events for each customer_id

  df_session['session_id'] = (df_session.groupby('event_customer-id')['session_start']
                      .cumsum().astype(int)+1)
  


  #np.savetxt(r'df.txt', df.values, fmt='%s')

  #print(df_session)


  #Database connection, create session table and copy df_sessions to table


  engine = create_engine('postgresql://username:password@localhost/mydatabase')
  
  try:
      connection = psycopg2.connect(database="mydatabase",
                        host="192.168.5.5",
                        user="postgres",
                        password="myPassword",
                        port="5432")
      cursor = connection.cursor()
      sql_query = "CREATE TABLE sessions (session_id INTEGER PRIMARY KEY,event_customer-id INTEGER NOT NULL,event_timestamp TIMESTAMP NOT NULL,type TEXT NOT NULL, time_delta TIMESTAMP NOT NULL, session_start BOOLEAN NOT NULLk, session_id INTEGER NOT NULL );"

      cursor.execute(sql_query)
      df_session.to_sql('sessions', engine, if_exists='replace')

  except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

    df_session.to_sql('sessions', engine, if_exists='replace')


  finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
    


#Create endpoint REST API



if __name__ == "__main__":
  execute()
