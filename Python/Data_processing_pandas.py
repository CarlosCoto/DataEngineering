# See instructions for installing Requests module for Python
# https://requests.readthedocs.io/en/master/user/install/#install

import pandas as pd
import numpy as np
import requests
import json
import psycopg2
from sqlalchemy import create_engine
import urllib.request

def execute():

  requestUrl = ""
  
  try:
   
    with urllib.request.urlopen(requestUrl) as f:
  
      data = [json.loads(line) for line in f]

    # Use json_normalize() to create a DataFrame

      df = pd.json_normalize(data, sep='_')

      print("Dataframe created with",len(df.columns),"columns:",df.columns, "and", len(df.index),"rows")

  except (Exception, urllib.Error) as error:
      print("Dataframe could not be created", error)

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
  

    
if __name__ == "__main__":
  execute()
