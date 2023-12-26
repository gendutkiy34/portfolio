import os
import cx_Oracle
from Modules.general import ReadJsonFile


def OracleConPd(patfile):
    json_cred=ReadJsonFile(patfile)
    try :
        connection = cx_Oracle.connect(user=json_cred['username'], password=json_cred['password'],
                               dsn=f"{json_cred['host']}:{json_cred['port']}/{json_cred['sid']}",
                               encoding="UTF-8")
    except Exception as e:
        connection="connection failed !!!!"  
        print(f'{connection} \nfailed due to :\n\n {e} \n\n') 
    return connection

