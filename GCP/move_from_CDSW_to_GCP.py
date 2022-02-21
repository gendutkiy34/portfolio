##########################################################################################
# Purpose   : move data from CDSW to GCP                                                 #
# Requestor : Mr. xxx                                                                    #
# Date      : xxxxxxxxxxx                                                                #
##########################################################################################

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

# Tidak dapat menginstall

############################## SparkSession Initialize
spark = SparkSession\
  .builder\
  .appName("TEST to GCP")\
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
################ Set Directory to load credentials file ################
import sys
sys.path.insert(1, '/BACA - REPO - BIG DATA 3/PLAYGROUND/HARIONO/test_gcp')

################################# set proxy #################################
import os 
proxy = '<proxy address>'
os.environ['https_proxy'] = proxy
os.environ['http_proxy'] = proxy

################# Set Credentials and project_id ################
credentials = service_account.Credentials.from_service_account_file('authentication_file.json')
project_id = '<project_id>'

pandas_gbq.context.credentials = credentials
pandas_gbq.context.project = "poc-ddb-mlops"

# Set Up Big Query Client
client = bigquery.Client(credentials= credentials, project=project_id)


###################################### Upload to GCP with  auto define table Schema GCP  ######################################
table_id_gcp = "<table_name_on_googlecloud>"
project_id_gcp = "<project_id_on_googlecloud>"

data_feature1=spark.sql("""
select distinct feature_1
from datamart.masked_sample_dataset_debitur_sme_cif_level_v2_2""")
list_ds=data_feature1.rdd.flatMap(lambda x: x).collect()

ds_error=[]
ds_success=[]
for ds in list_ds :
  df_dataset=spark.sql("""
  select * 
  from datamart.masked_sample_dataset_debitur_sme_cif_level_v2_2
  where feature_1 = '{}'""".format(ds))
  dataset_masked = df_dataset.toPandas()
  try :
    pandas_gbq.to_gbq(dataset_masked,table_id,
                      project_id = project_id , if_exists = 'append')
    del dataset_masked
    ds_success.append(ds)
    print(ds,'succes to GCP')
  except Exception  as e :
    ds_error.append(ds)
    print(ds,'failed to GCP')
    
###################################### Upload to GCP with define manual table Schema GCP ######################################    
gcp_schema=[{"name":"feature_0","type":"STRING"},
{"name":"target","type":"INTEGER"},
{"name":"feature_3","type":"INTEGER"},
{"name":"feature_4","type":"INTEGER"},
{"name":"feature_5","type":"INTEGER"},
{"name":"feature_6","type":"STRING"},
{"name":"feature_7","type":"INTEGER"},
{"name":"feature_8","type":"STRING"},
{"name":"feature_9","type":"STRING"},
{"name":"feature_10","type":"STRING"},
{"name":"feature_11","type":"STRING"},
{"name":"feature_12","type":"STRING"},
{"name":"feature_13","type":"STRING"},
{"name":"feature_14","type":"STRING"},
{"name":"feature_15","type":"STRING"},
{"name":"feature_16","type":"STRING"},
{"name":"feature_17","type":"STRING"},
{"name":"feature_18","type":"STRING"},
{"name":"feature_19","type":"STRING"},
{"name":"feature_20","type":"INTEGER"},
{"name":"feature_21","type":"STRING"},
{"name":"feature_22","type":"STRING"},
{"name":"feature_23","type":"STRING"},
{"name":"feature_24","type":"STRING"},
{"name":"feature_25","type":"FLOAT"},
{"name":"feature_26","type":"INTEGER"},
{"name":"feature_27","type":"INTEGER"},
{"name":"feature_28","type":"STRING"},
{"name":"feature_29","type":"FLOAT"},
{"name":"feature_30","type":"FLOAT"},
{"name":"feature_31","type":"FLOAT"},
{"name":"feature_32","type":"FLOAT"},
{"name":"feature_33","type":"FLOAT"},
{"name":"feature_34","type":"FLOAT"},
{"name":"feature_35","type":"FLOAT"},
{"name":"feature_36","type":"FLOAT"},
{"name":"feature_37","type":"FLOAT"},
{"name":"feature_38","type":"FLOAT"},
{"name":"feature_39","type":"FLOAT"},
{"name":"feature_40","type":"FLOAT"},
{"name":"feature_41","type":"FLOAT"},
{"name":"feature_42","type":"FLOAT"},
{"name":"feature_43","type":"FLOAT"},
{"name":"feature_44","type":"FLOAT"},
{"name":"feature_45","type":"FLOAT"},
{"name":"feature_46","type":"FLOAT"},
{"name":"feature_47","type":"FLOAT"},
{"name":"feature_48","type":"FLOAT"},
{"name":"feature_49","type":"FLOAT"},
{"name":"feature_50","type":"FLOAT"},
{"name":"feature_51","type":"FLOAT"},
{"name":"feature_52","type":"FLOAT"},
{"name":"feature_53","type":"FLOAT"},
{"name":"feature_54","type":"FLOAT"},
{"name":"feature_55","type":"STRING"},
{"name":"feature_56","type":"STRING"},
{"name":"feature_57","type":"STRING"},
{"name":"feature_58","type":"STRING"},
{"name":"feature_59","type":"STRING"},
{"name":"feature_60","type":"STRING"},
{"name":"feature_61","type":"STRING"},
{"name":"feature_62","type":"STRING"},
{"name":"feature_63","type":"STRING"},
{"name":"feature_64","type":"STRING"},
{"name":"feature_65","type":"STRING"},
{"name":"feature_66","type":"STRING"},
{"name":"feature_67","type":"STRING"},
{"name":"feature_68","type":"STRING"},
{"name":"feature_69","type":"STRING"},
{"name":"feature_70","type":"STRING"},
{"name":"feature_71","type":"STRING"},
{"name":"feature_72","type":"STRING"},
{"name":"feature_73","type":"STRING"},
{"name":"feature_74","type":"STRING"},
{"name":"feature_75","type":"STRING"},
{"name":"feature_76","type":"STRING"},
{"name":"feature_77","type":"STRING"},
{"name":"feature_78","type":"STRING"},
{"name":"feature_79","type":"FLOAT"},
{"name":"feature_80","type":"FLOAT"},
{"name":"feature_81","type":"FLOAT"},
{"name":"feature_82","type":"FLOAT"},
{"name":"feature_83","type":"FLOAT"},
{"name":"feature_84","type":"FLOAT"},
{"name":"feature_85","type":"FLOAT"},
{"name":"feature_86","type":"FLOAT"},
{"name":"feature_87","type":"STRING"},
{"name":"feature_88","type":"STRING"},
{"name":"feature_89","type":"STRING"},
{"name":"feature_90","type":"STRING"},
{"name":"feature_91","type":"STRING"},
{"name":"feature_92","type":"STRING"},
{"name":"feature_93","type":"STRING"},
{"name":"feature_94","type":"STRING"},
{"name":"feature_95","type":"STRING"},
{"name":"feature_96","type":"STRING"},
{"name":"feature_97","type":"STRING"},
{"name":"feature_98","type":"STRING"},
{"name":"feature_99","type":"FLOAT"},
{"name":"feature_100","type":"FLOAT"},
{"name":"feature_101","type":"FLOAT"},
{"name":"feature_102","type":"FLOAT"},
{"name":"feature_103","type":"FLOAT"},
{"name":"feature_104","type":"FLOAT"},
{"name":"feature_105","type":"FLOAT"},
{"name":"feature_106","type":"FLOAT"},
{"name":"feature_107","type":"FLOAT"},
{"name":"feature_108","type":"FLOAT"},
{"name":"feature_109","type":"FLOAT"},
{"name":"feature_110","type":"FLOAT"},
{"name":"feature_111","type":"STRING"},
{"name":"feature_112","type":"STRING"},
{"name":"feature_113","type":"STRING"},
{"name":"feature_114","type":"STRING"},
{"name":"feature_115","type":"STRING"},
{"name":"feature_116","type":"STRING"},
{"name":"feature_117","type":"STRING"},
{"name":"feature_118","type":"STRING"},
{"name":"feature_119","type":"STRING"},
{"name":"feature_120","type":"STRING"},
{"name":"feature_121","type":"STRING"},
{"name":"feature_122","type":"STRING"},
{"name":"feature_123","type":"FLOAT"},
{"name":"feature_124","type":"FLOAT"},
{"name":"feature_125","type":"FLOAT"},
{"name":"feature_126","type":"FLOAT"},
{"name":"feature_127","type":"STRING"},
{"name":"feature_128","type":"STRING"},
{"name":"feature_129","type":"STRING"},
{"name":"feature_130","type":"STRING"},
{"name":"feature_131","type":"STRING"},
{"name":"feature_132","type":"STRING"},
{"name":"feature_133","type":"STRING"},
{"name":"feature_134","type":"STRING"},
{"name":"feature_135","type":"STRING"},
{"name":"feature_136","type":"STRING"},
{"name":"feature_137","type":"STRING"},
{"name":"feature_138","type":"STRING"},
{"name":"feature_139","type":"STRING"},
{"name":"feature_140","type":"STRING"},
{"name":"feature_141","type":"STRING"},
{"name":"feature_142","type":"STRING"},
{"name":"feature_143","type":"STRING"},
{"name":"feature_144","type":"STRING"},
{"name":"feature_145","type":"STRING"},
{"name":"feature_146","type":"STRING"},
{"name":"feature_147","type":"STRING"},
{"name":"feature_148","type":"STRING"},
{"name":"feature_149","type":"STRING"},
{"name":"feature_150","type":"STRING"},
{"name":"feature_151","type":"STRING"},
{"name":"feature_152","type":"STRING"},
{"name":"feature_153","type":"STRING"},
{"name":"feature_154","type":"INTEGER"},
{"name":"feature_155","type":"INTEGER"},
{"name":"feature_156","type":"INTEGER"},
{"name":"feature_157","type":"INTEGER"},
{"name":"feature_158","type":"FLOAT"},
{"name":"feature_159","type":"INTEGER"},
{"name":"feature_160","type":"INTEGER"},
{"name":"feature_161","type":"INTEGER"},
{"name":"feature_162","type":"INTEGER"},
{"name":"feature_163","type":"INTEGER"},
{"name":"feature_164","type":"INTEGER"},
{"name":"feature_165","type":"INTEGER"},
{"name":"feature_166","type":"INTEGER"},
{"name":"feature_167","type":"INTEGER"},
{"name":"feature_168","type":"INTEGER"},
{"name":"feature_1","type":"STRING"}]
    
df_dataset=spark.sql("""
select * 
from datamart.masked_sample_dataset_debitur_sme_cif_level_v2_2
where feature_1 in ('201609')""")
dataset_masked = df_dataset.toPandas()

try :
  pandas_gbq.to_gbq(dataset_masked,table_id,
                    project_id = project_id , if_exists = 'append',table_schema=gcp_schema)
  del dataset_masked
  print('201609 succes to GCP')
except Exception  as e :
  print('201609 failed to GCP')
  