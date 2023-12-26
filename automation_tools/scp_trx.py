import os
import pandas as pd
import base64
from datetime import datetime, timedelta,time
from Modules.general import ReadJsonFile,ReadTxtFile,ConvertStrtoDate,ConvertDatetoStr,BarChart,PrintScpCdr
from Modules.readconfig import ConfigScm,AllConfig

#CONFIG
pd.set_option('display.max_rows', None)

#VARIABLE
basedir=os.path.abspath(os.path.dirname(__file__))
sdpcdr=f'{basedir}/Connection/scp_cdr_mm.json'
scpsit=f'{basedir}/Connection/scp_cdr_sit.json'
txtnotfound='\t\t\tDATA NOT FOUND !!!'
grs='-'*47  
grs2='='*47


#CDR TRX
def CdrTrx():
    hp=input('FILL MSISDN           : ')
    dt=input('FILL DATE (dd-mm-yyyy): ')
    dtsplit=dt.split('-')
    if hp[0] == '0' :
        msisdn=hp[1:]
    else :
        msisdn=hp[2:]
    sqltxt=f'{basedir}/sql/scpcdr.sql'
    sql=ReadTxtFile(pathfile=sqltxt)
    conscp=AllConfig(connectionpath=sdpcdr)
    sqlfull=sql.format(msisdn=msisdn,mon=dtsplit[1],day=dtsplit[0],string_connection=conscp.VerifyConn())
    dictcdr=conscp.Queryall(sqltext=sqlfull)
    if dictcdr :
        df=pd.DataFrame(dictcdr)
        dfdisp=df[['CDR_HOUR','TRANSACTION_ID','CALLING_PARTY','CALLED_PARTY','DIAMETER_RESULT_CODES','CALL_DURATION','CALL_TYPE','CALL_STATUS','INSTANCE_ID']]
        os.system('clear')
        os.system('clear')
        print(f'\n\nCDR DATE : {dictcdr[0]["CDR_DATE"]}\n{grs2}{grs2}{grs2}\n{dfdisp}\n{grs2}{grs2}{grs2}\n\n')
        trxid=input("fill transaction id for detail\n(use ';' as delimeter for more than one ) : ")
        print('\n')
        list_trxid=trxid.split(';')
        dftemp=df[df['TRANSACTION_ID'].isin(list_trxid) ]
        if len(dftemp.index) != 0:
            dicttrxid=dftemp.to_dict('records')
            for d in dicttrxid:
                PrintScpCdr(d)
        else :
            print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')
    else :
        print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')


#CDR TRX SIT
def TrxSit():
    hp=input('FILL MSISDN           : ')
    dt=input('FILL DATE (dd-mm-yyyy): ')
    dtsplit=dt.split('-')
    if hp[0] == '0' :
        msisdn=hp[1:]
    else :
        msisdn=hp[2:]
    sqltxt=f'{basedir}/sql/scpcdr_sit.sql'
    sql=ReadTxtFile(pathfile=sqltxt)
    conscp=AllConfig(connectionpath=scpsit)
    sqlfull=sql.format(msisdn=msisdn,mon=dtsplit[1],day=dtsplit[0],string_connection=conscp.VerifyConn())
    dictcdr=conscp.Queryall(sqltext=sqlfull)
    if dictcdr :
        df=pd.DataFrame(dictcdr)
        dfdisp=df[['CDR_HOUR','TRANSACTION_ID','CALLING_PARTY','CALLED_PARTY','DIAMETER_RESULT_CODES','CALL_DURATION','CALL_TYPE','CALL_STATUS','INSTANCE_ID']]
        os.system('clear')
        os.system('clear')
        print(f'\n\nCDR DATE : {dictcdr[0]["CDR_DATE"]}\n{grs2}{grs2}{grs2}\n{dfdisp}\n{grs2}{grs2}{grs2}\n\n')
        trxid=input("fill transaction id for detail\n(use ';' as delimeter for more than one ) : ")
        print('\n')
        list_trxid=trxid.split(';')
        dftemp=df[df['TRANSACTION_ID'].isin(list_trxid) ]
        if len(dftemp.index) != 0:
            dicttrxid=dftemp.to_dict('records')
            for d in dicttrxid:
                PrintScpCdr(d)
        else :
            print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')
    else :
        print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')


#diameter daily trend
def DailyTrend():
    diameter=input('Diameter Error Code     : ')
    dt1=input('Start Date (dd-mm-yyyy) : ')
    dt2=input('Stop Date  (dd-mm-yyyy) : ')
    stt=datetime.strptime(dt1,'%d-%m-%Y').date()
    stp=datetime.strptime(dt2,'%d-%m-%Y').date()
    sqltxt=f'{basedir}/sql/diameter_daily.sql'
    sql=ReadTxtFile(pathfile=sqltxt)
    conscp=AllConfig(connectionpath=sdpcdr)
    list_x=[]
    list_y=[]
    list_raw=[]
    if diameter is not None and dt1 is not None and dt2 is not None :
        while stt <= stp :
            day=stt.strftime("%d")
            mon=stt.strftime("%m")
            day_mon=f'{day}-{mon}'
            sqlfull=sql.format(day=day,mon=mon,diameter=diameter,string_connection=conscp.VerifyConn())
            dictcontent=conscp.Queryall(sqltext=sqlfull)
            list_x.append(day_mon)
            list_y.append(int(dictcontent[0]['TOTAL']))
            list_raw.append(dictcontent[0])
            print(f'date {day} done')
            stt += timedelta(days=1)
        df=pd.DataFrame(list_raw)
        opt=input('\n Show in graph (Y/N ) : ')
        if str(opt).lower() == "y" :
            os.system('clear')
            os.system('clear')
            print('\n')
            title_chart=f'Diameter {diameter} daily trend'
            BarChart(x=list_x,y=list_y,title=title_chart)
            print(f'\n\nDIAMETER : {diameter} - Daily Trend\n{grs2}\n{df}\n{grs2}\n\n')
        else :
            os.system('clear')
            os.system('clear')
            print(f'\nDIAMETER : {diameter} - Daily Trend\n{grs2}\n{df}\n{grs2}\n\n')
    else :
        print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')
    
    
#diameter daily trend
def BftTrx():
    dt=input('Date (dd-mm-yyyy)   : ')
    hr=input('Hour (HH24)         : ')
    sqltxt=f'{basedir}/sql/bft_trx.sql'
    sql=ReadTxtFile(pathfile=sqltxt)
    conscp=AllConfig(connectionpath=sdpcdr)
    if dt is not None  and hr is not None :
        dtsplit=dt.split('-')
        sqlfull=sql.format(day=dtsplit[0],mon=dtsplit[1],hour=hr,string_connection=conscp.VerifyConn())
        dictcontent=conscp.Queryall(sqltext=sqlfull)
        df=pd.DataFrame(dictcontent)
        dfbft=df[['CDR_HOUR','TRANSACTION_ID','CALLING_PARTY','DIAMETER_RESULT_CODES','CALL_DURATION','CALL_STATUS','CALL_TYPE','SUB_CALL_TYPE']]
        os.system('clear')
        os.system('clear')
        print(f'\n\nCDR DATE : {df.at[0, "CDR_DATE"]}\n{grs2}{grs2}{grs2}\n{dfbft}\n{grs2}{grs2}{grs2}\n\n')
        trxid=input("fill transaction id for detail\n(use ';' as delimeter for more than one ) : ")
        print('\n')
        list_trxid=trxid.split(';')
        dftemp=df[df['TRANSACTION_ID'].isin(list_trxid) ]
        if len(dftemp.index) != 0:
            dicttrxid=dftemp.to_dict('records')
            for d in dicttrxid:
                PrintScpCdr(d)
    else :
        print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')