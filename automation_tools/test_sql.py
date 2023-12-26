# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 23:31:13 2023

@author: HS00935501
"""

import pandas as pd
import time
import os
import schedule
from datetime import datetime, timedelta
from modules.general import GetToday
from modules.connection import OracleCon
from modules.general import ReadJsonFile,ReadTxtFile,ConvertListToDict,GetToday,ConvertDatetoStr,Sum2list
from GrepDataNew import GetDataMinute


def ScpMinute():
    pathdir=os.getcwd()
    outputfile=f'{pathdir}/rawdata/scp_newdata_minute.csv'
    conpath=(f'{pathdir}/connections/scpprodtrx.json')
    sqltxt=ReadTxtFile(f'{pathdir}/sql/scpminute2.sql')
    today=GetToday()
    list_day=[0]
    list_newdata=[]
    for dy in list_day:
        dt=today - timedelta(days=dy)
        data=GetDataMinute(pathsql=sqltxt,pathconnection=conpath,dat=dt)
        df=pd.DataFrame(data)
        df['REMARK']=f'day{dy}'
        datanew=df.to_dict('records')
        for dn in datanew:
            list_newdata.append(dn)
