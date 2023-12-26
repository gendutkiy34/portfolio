# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 14:08:47 2023

@author: HS00935501
"""

import pandas as pd
import os
import json
from datetime import datetime,timedelta
from Modules.general import ReadJsonFile,ReadTxtFile,ConvertStrtoDate,ConvertDatetoStr
from Modules.readconfig import AllConfig


#variable
basedir=os.path.abspath(os.path.dirname(__file__))
scptrx=f'{basedir}/Connection/scp_cdr_mm.json'
txtnotfound='\t\t\tDATA NOT FOUND !!!'
grs='-'*50


def CustScpCdrQue():
    startdate=input('date start (dd-mm-yyyy) : ')
    enddate=input('date stop (dd-mm-yyyy) : ')
    sqlpath=input('please fill full sql script path : ')
    outputpath=input('please fill name output (output in csv): ')
    sql=ReadTxtFile(pathfile=sqlpath)
    conscp=AllConfig(connectionpath=scptrx)
    if startdate is not None and enddate is not None and sqlpath is not None :
        stt=datetime.strptime(startdate,'%d-%m-%Y').date()
        stp=datetime.strptime(enddate,'%d-%m-%Y').date()
        list_raw=[]
        while stt <= stp :
            day=stt.strftime("%d")
            mon=stt.strftime("%m")
            sqlfull=sql.format(day=day,mon=mon,string_connection=conscp.VerifyConn())
            dictcust=conscp.Queryall(sqltext=sqlfull)
            [list_raw.append(t) for t in dictcust]
            print(f"date {stt.strftime('%d-%m-%Y')} done")
            stt += timedelta(days=1)
        if list_raw:
            df=pd.DataFrame(list_raw)
            df.to_csv(f'/home/scpsdpdev/clitool/output/{outputpath}.csv')
            print (f'{grs}{grs}\n\t\t\t\t/home/scpsdpdev/clitool/output/{outputpath}.csv\n{grs}{grs}')
        else :
            print (f'{grs}{grs}\n\t\t\t\tDATA NOT FOUND !!!!!\n{grs}{grs}')
    else :
        print (f'{grs}{grs}\n\t\t\t\tDATA NOT FOUND !!!!!\n{grs}{grs}')
    