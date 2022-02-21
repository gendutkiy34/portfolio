###################################### Import Library ###################################### 
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql import Window
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.rdd import reduce
from pyspark.sql.utils import AnalysisException, ParseException
import pandas as pd
import logging
import warnings
import re
from time import sleep
from datetime import datetime

################# import google library ####################
from google.oauth2 import service_account
from google.cloud import storage
from google.cloud import bigquery
import pandas_gbq

############################## SparkSession Initialize
spark = SparkSession\
  .builder\
  .appName("Test Read GCP")\
  .config("spark.dynamicAllocation.enabled", "false")\
  .config("spark.executor.instances", "4")\
  .config("spark.executor.cores", "4")\
  .config("spark.executor.memory", "8g")\
  .config("spark.network.timeout", 60)\
  .config("spark.yarn.executor.memoryOverhead", "8g")\
  .config("spark.sql.parquet.compression.codec", "snappy")\
  .config("spark.network.timeout", 3000) \
  .config("spark.sql.sources.partitionColumnTypeInference.enabled", "false")\
  .config("spark.ui.showConsoleProgress","false")\
  .config("spark.serializer","org.apache.spark.serializer.KryoSerializer")\
  .config("spark.kryoserializer.buffer.max","1024m")\
  .enableHiveSupport()\
  .getOrCreate()
  
  # .config("spark.driver.maxResultSize","2g")\
################################# Set Directory to load credentials file #################################
import sys
sys.path.insert(1, '/BACA - REPO - BIG DATA 3/PLAYGROUND/HARIONO/test_gcp')

################################################## set proxy ##################################################
import os 
proxy = 'http://proxy2.bri.co.id:1707'
os.environ['https_proxy'] = proxy
os.environ['http_proxy'] = proxy

################################## Set Credentials and project_id #################################
credentials = service_account.Credentials.from_service_account_file('authentication_file.json')
project_id_gcp = '<project_id_gcp>'

pandas_gbq.context.credentials = credentials
pandas_gbq.context.project = "project_id_gcp"

################################## Set Up Big Query Client ##################################
client = bigquery.Client(credentials= credentials, project=project_id)

###################################### Processs ######################################
table_id_gcp = "<table_id_gcp>"
project_id_gcp = "<project_id_gcp>"  

gcp_sql="""select * 
from  {}.{}
limit 20""".format(project_id_gcp,table_id_gcp)

df_read_gcp=pd.read_gbq(gcp_sql,dialect="standard")

