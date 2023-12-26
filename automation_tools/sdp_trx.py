# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 17:16:23 2023

@author: HS00935501
"""

import os
import pandas as pd
import base64
from datetime import datetime, timedelta,time
from Modules.general import ReadJsonFile,ReadTxtFile,ConvertStrtoDate,ConvertDatetoStr
from Modules.readconfig import ConfigScm,AllConfig

#CONFIG
pd.set_option('display.max_rows', None)


#VARIABLE
basedir=os.path.abspath(os.path.dirname(__file__))
sdpcdr=f'{basedir}/Connection/sdp_cdr_mm.json'
txtnotfound='\t\t\tDATA NOT FOUND !!!'
list_accflag=['66','67','68','72','73']


#CDR TRX
def CdrTrx():
    grs='-'*47  
    grs2='='*47
    hp=input('FILL MSISDN           : ')
    dt=input('FILL DATE (dd-mm-yyyy): ')
    dtsplit=dt.split('-')
    if hp[0] == '0' :
        msisdn=hp[1:]
    else :
        msisdn=hp[2:]
    sqltxt=f'{basedir}/sql/sdpcdr.sql'
    sql=ReadTxtFile(pathfile=sqltxt)
    consdp=AllConfig(connectionpath=sdpcdr)
    sqlfull=sql.format(msisdn=msisdn,mon=dtsplit[1],day=dtsplit[0],string_connection=consdp.VerifyConn())
    dictcdr=consdp.Queryall(sqltext=sqlfull)
    if len(dictcdr) != 0 :
        df=pd.DataFrame(dictcdr)
        dfdisp=df[['CDRTIME','CLIENTTRANSACTIONID','TRANSACTIONID','INTERNALCAUSE','BASICCAUSE','PRICE','SHORTCODE','KEYWORD','NETWORKMODE']]
        os.system('clear')
        os.system('clear')
        print(f'\n\nCDR DATE : {dictcdr[0]["CDRDATE"]} \t MSISDN : 62{dictcdr[0]["MSISDN"]}\n{grs2}{grs2}{grs2}\n{dfdisp}\n{grs2}{grs2}{grs2}\n\n')
        trxid=input("fill transaction id for detail\n(use ';' as delimeter for more than one ) : ")
        print('\n')
        list_trxid=trxid.split(';')
        dftemp=df[(df['TRANSACTIONID'].isin(list_trxid)) & (df['ACCESSFLAG'].isin(list_accflag)) ]
        #RESERVE_BALANCE_CBS_ERRORCODE=2001;CP_NOTIFICATION_ERRORCODE=200;DEBIT_BALANCE_CBS_ERRORCODE=2001  
        if len(dftemp.index) != 0:
            dicttrxid=dftemp.to_dict('records')
            for d in dicttrxid:
                if 'CP_NOTIFICATION_ERRORCODE' in d["THIRDPARTYERRORCODE"] and 'DEBIT_BALANCE_CBS_ERRORCODE' in d["THIRDPARTYERRORCODE"]:
                    temp=d["THIRDPARTYERRORCODE"].split(';')
                    temp1=[t.split('=') for t in temp]
                    cpnotif=temp1[1]
                    txtdiameter=f"{d['INTERNALCAUSE']} ( COMMIT )"
                elif 'DEBIT_BALANCE_CBS_ERRORCODE' in d["THIRDPARTYERRORCODE"] and 'CP_NOTIFICATION_ERRORCODE' not in d["THIRDPARTYERRORCODE"]:
                    cpnotif='-'
                    txtdiameter=f"{d['INTERNALCAUSE']} ( COMMIT )"
                else :
                    cpnotif='-'
                    txtdiameter=f"{d['INTERNALCAUSE']} ( RESERVE )"
                txt=f"""{grs} {d['TRANSACTIONID']} {grs}
CDR DATE  : {d['CDRDATE']}
CDR TIME  : {d['CDRTIME']}
TRX ID    : {d['TRANSACTIONID']}
CLIENT ID : {d['CLIENTTRANSACTIONID']}
MSISDN    : {d['MSISDN']}
DIAMETER  : {txtdiameter} 
BASICCAUSE: {d['BASICCAUSE']}
CP ID     : {d['CP_ID']}
CP NAME   : {d['CP_NAME']}
SHORTCODE : {d['SHORTCODE']}
OFFERCODE : {d['OFFERCODE']}
PRICE     : {d['PRICE']}
KEYWORD   : {d['KEYWORD']}
OPER TYPE : {d['NETWORKMODE']}
CATEGORY  : {d['CATEGORYID']}
CP RESPONS: {cpnotif}
CHANEL    : {d['CHANNEL']}
CP LOGIN  : {d['CP_LOGINNAME']}
TASK ID   : {d['TASKID']}
{grs}{grs}\n"""
                print(txt)
                


        
