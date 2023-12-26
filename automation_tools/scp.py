# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 14:28:36 2023

@author: HS00935501
"""

import pandas as pd
import os
import json
from datetime import datetime,timedelta
from Modules.general import ReadJsonFile,ReadTxtFile,ConvertStrtoDate,ConvertDatetoStr
from Modules.readconfig import AllConfig
from custom_query import CustScpCdrQue
from Modules.general import Banner
from scp_trx import CdrTrx,DailyTrend,BftTrx,TrxSit
from find_log import Scplog



#SETTING
pd.set_option('display.max_rows', None)

#VARIABLE
textbanner="SDP - SCP OPS TEAM"
grs="="*130
grs2="-"*130


os.system('clear')
print (f'{grs}\n')
Banner(textbanner)
print (f'\n{grs}')
head="""
1.  SCP - CDR PROD                              
2.  SCP - CDR SIT
3.  SCP - DIAMETER DAILY TREND
4.  SCP - BFT TRX 
5.  LOG - SCP
Please choose one : 
"""
opt=input(head)

if opt == "1":
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tCHECK CDR SDP PROD\n{grs2}"
    Banner(textbanner)
    print(info)
    CdrTrx()      
elif opt == "2":
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tCHECK CDR SDP SIT\n{grs2}"
    Banner(textbanner)
    print(info)
    TrxSit()   
elif opt == "3":
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tCHECK DIAMETER DAILY TREND\n{grs2}"
    Banner(textbanner)
    print(info)
    DailyTrend()  
elif opt == "4":
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tCHECK BFT TRX\n{grs2}"
    Banner(textbanner)
    print(info)
    BftTrx()
elif opt == "5":
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tFIND SCP LOG\n{grs2}"
    Banner(textbanner)
    print(info)
    #Scplog()
else :
    print ('WRONG INPUT !!!')