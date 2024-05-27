import pandas as pd
import json
import psycopg2
from sqlalchemy import create_engine
import urllib.request
from urllib.parse import quote_plus

def DataToDB():

  requestUrl = "https://storage.googleapis.com/xcc-de-assessment/events.json"
  
  try:
     
    with urllib.request.urlopen(requestUrl) as f:

      data = [json.loads(line) for line in f]

    # Use json_normalize() to create a DataFrame flattening json (creates new columns for nested values with _ as string separator)

      df = pd.json_normalize(data, sep='_') 

    #print df info

      print("Dataframe created with",len(df.columns),"columns:",df.columns, "and", len(df.index),"rows")

  except (Exception, urllib.Error) as error:
      print("Dataframe could not be created", error)  

  #filter on not-null customer-ids

  df = df[df['event_customer-id'].notnull()]

  df=df.rename(columns={'event_customer-id':'event_customer_id'})

  #convert timestamp to datetime format

  df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])

  df = df.sort_values('event_timestamp')

  #create session dataframe copying desired columns

  df_session = df[['event_customer_id', 'event_timestamp', 'type']].copy()

  #calculate time delta for each customer_id session

  df_session['time_delta'] = (df_session.groupby('event_customer_id')['event_timestamp']
                      .diff().fillna(str(pd.Timedelta(seconds=0))))


  # Identify session start events (delta greater than 30 minutes)
  df_session['session_start'] = (df_session['time_delta'] > pd.Timedelta(minutes=30))

    # Calculate session IDs using cumsum of session_start events for each customer_id

  df_session['session_id'] = (df_session.groupby('event_customer_id')['session_start']
                      .cumsum().astype(int)+1)
  
  print("Dataframe sessions (client-id not null) created with",len(df_session.columns),"columns:",df_session.columns, "and", len(df_session.index),"rows")
 
 #Database connection, create session table and copy df_sessions to table

  engine = create_engine('postgresql://postgres:%s@localhost/postgres' % quote_plus('SachaBose1969@'))

  
  try:
      connection = psycopg2.connect(
                        database='postgres',
                        host='localhost',
                        user='postgres',
                        password='SachaBose1969@', #needs to be secured
                        port='5432')
      cursor = connection.cursor()

      #create table in DB (if not exist)
      sql_query = "CREATE TABLE IF NOT EXISTS sessions (session_id INTEGER PRIMARY KEY,event_customer_id INTEGER NOT NULL,event_timestamp TIMESTAMP NOT NULL,type TEXT NOT NULL, time_delta TIMESTAMP NOT NULL, session_start BOOLEAN NOT NULL );"

      #sql_query = "CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY);"
      cursor.execute(sql_query)

      sql_query = 'INSERT INTO public."SessionsApp_sessions" SELECT index, event_customer_id, MAX(session_id-1), AVG(time_delta) FROM public.sessions WHERE type = \'placed_order\' GROUP BY event_customer_id, index ORDER BY event_customer_id;'

      cursor.execute(sql_query)

      cursor.close()
      connection.commit()
      #df_session.to_sql('sessions', engine, if_exists='replace')

  except (Exception, psycopg2.DatabaseError) as error:
    print("Error while fetching data from PostgreSQL", error)

  try:
    df_session.to_sql('sessions', engine, schema='public', if_exists='replace')
  except (Exception, psycopg2.Error) as error:
    print ("Data not added to DB", error)
  
  finally:
    if connection:
        cursor.close()
        connection.close()
        print("Data added to sessions table in PostgresSQL database",)
        print("PostgreSQL connection is closed")

  return("Dataframe created and copied to DB")
  
#Create endpoint REST API
