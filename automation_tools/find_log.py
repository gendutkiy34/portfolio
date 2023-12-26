# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 17:42:36 2023

@author: HS00935501
"""

import os
import pandas as pd
import base64
from base64 import b64encode
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime, timedelta,time
from Modules.general import GetToday,ReadJsonFile,ReadTxtFile,ConvertStrtoDate,ConvertDatetoStr,SshNode
from Modules.readconfig import ConfigScm,AllConfig


#credential
scplogcred='/home/scpsdpdev/clitool/Scripts/Connection/scplog.json'
sdpprovcred='/home/scpsdpdev/clitool/Scripts/Connection/sdpprov.json'
sdplogs='/home/scpsdpdev/clitool/Scripts/Connection/sdplog.json'
grs="="*130
grs2="-"*130


#SCP log
def ScpLog():
    trxid=input('Fill Transaction ID   : ')
    dtstr=input('Fill date (dd-mm-yyyy): ')
    td=GetToday()
    dt=ConvertStrtoDate(dtstr,'%d-%m-%Y')
    cred=ReadJsonFile(scplogcred)
    if trxid is not None and dtstr is not None :
        dataraw=[]
        if dt.date() == td.date() :
            for c in cred:
                print(f"login {c['host']} ...")
                dtstring1=ConvertDatetoStr(dt,'%Y%m%d')
                dtstring2=ConvertDatetoStr(dt,'%Y-%m-%d')
                cmd=f'grep -ah {trxid} /opt/logs/scp_app/*{dtstring1}*;zgrep -ah {trxid} /opt/logs/scp_app/*{dtstring2}*'
                datatemp=SshNode(host=c['host'],user=c['username'],pwd=c['password'],cmd=cmd)       
                data=datatemp.decode('ascii').split('\n')
                for d in data :
                    dataraw.append(d)
        else :
            for c in cred:
                print(f"login {c['host']} ...")
                dtstring2=ConvertDatetoStr(dt,'%Y-%m-%d')
                cmdn=f'ls /opt/logs/scp_app/ | grep {dtstring2} | wc -l'
                ndata=SshNode(host=c['host'],user=c['username'],pwd=c['password'],cmd=cmdn)
                n=str(ndata.decode('ascii')).replace('\n','')
                if int(n) > 0 :
                    cmd=f'zgrep -ah {trxid} /opt/logs/scp_app/*{dtstring2}*'
                    datatemp=SshNode(host=c['host'],user=c['username'],pwd=c['password'],cmd=cmd)
                    data=datatemp.decode('ascii').split("\n")
                    for t in data:
                        dataraw.append(data) 
                else :
                    txterr=f'log file {dtstr} not available on log server'
        data_clean=[]
        dataclean2=[]
        if dataraw :
            for d in dataraw :
                if d is not None or d !=  '' :
                    try :
                        djson=json.loads(d)
                        txt=f"{djson['logData']['data']['TimeStamp']} - {djson['logData']['data']['EventTID']} - {djson['logData']['data']['EventType']} - {djson['logData']['data']['EventCategory']} : {djson['logData']['data']['EventMessage']}"
                        data_clean.append(txt)
                    except Exception :
                        pass
            for c in sorted(data_clean):
                dataclean2.append(c)
            txtfinal='\n'.join(dataclean2)    
        else :
            txtfinal='data not found !!!!'
        os.system("clear")
        os.system("clear")
        print (f'{grs}\n\t\t\t\t\t\tSCP LOG - {trxid}\n{grs}\n\n{txtfinal}\n\n{grs}')
    else :
        os.system("clear")
        os.system("clear")
        print (f'{grs}\n\t\t\t\tPlease check your input!!!!!\n{grs}')
    

#SDP BILLING LOG
def SdpSV():
    ssnid=input('Fill Billing Session ID   : ')
    dtstr=input('Fill date (dd-mm-yyyy)    : ')
    td=GetToday()
    dt=ConvertStrtoDate(dtstr,'%d-%m-%Y')
    #cred=ReadJsonFile(sdpprovcred)
    cred2=ReadJsonFile(sdplogs)
    txtfinal=""
    if ssnid is not None and dtstr is not None : 
        dtstring1=ConvertDatetoStr(dt,'%Y-%m-%d')
        if dt.date() == td.date() :
            print(f"login {cred2['host']} ...")
            cmd=f"grep -ah {ssnid} /logs01/BILLING/*{dtstring1}* | grep -v Processing"
            data=SshNode(host=cred2['host'],user=cred2['username'],pwd=cred2['password'],cmd=cmd)
        else :
            print(f"login {cred2['host']} ...")
            cmdn=f'ls /logs01/BILLING/backup/ | grep {dtstring1} | wc -l'
            ndata=SshNode(host=cred2['host'],user=cred2['username'],pwd=cred2['password'],cmd=cmdn)
            n=str(ndata.decode('ascii')).replace('\n','')
            if int(n) > 0 :
                cmd=f"zrep -ah {ssnid} /logs01/BILLING/backup/*{dtstring1}* | grep -v Processing"
                data=SshNode(host=cred2['host'],user=cred2['username'],pwd=cred2['password'],cmd=cmd)
            else :
                txtfinal=f'log file {dtstr} not available on log server'
        try :
            raw_data=data.decode('ascii').split("\n")
            data_clean=[]
            if raw_data :
                for d in raw_data :
                    if d is not None or d !=  '' :
                        data_clean.append(d)
                txtfinal='\n'.join(data_clean)
        except Exception :
            pass
        os.system("clear")
        os.system("clear")
        print (f'{grs}\n\t\t\t\t\t\tBILLING LOG - {ssnid}\n{grs}\n\n{txtfinal}\n\n{grs}')
    else :
        os.system("clear")
        os.system("clear")
        print (f'{grs}\n\t\t\t\tPlease check your input!!!!!\n{grs}')
        

#SCM LOG
def ScmLog():
    trxid=input('Fill Transaction    ID    : ')
    dtstr=input('Fill date (dd-mm-yyyy)    : ')
    td=GetToday()
    dt=ConvertStrtoDate(dtstr,'%d-%m-%Y')
    cred=ReadJsonFile(sdplogs)
    txtfinal=""
    if trxid is not None and dtstr is not None : 
        dtstring1=ConvertDatetoStr(dt,'%Y-%m-%d')
        print(f"login {cred['host']} ...")
        if dt.date() == td.date() : #today
            cmd=f"grep -ah {trxid} /logs01/SCM/*{dtstring1}*"
            data=SshNode(host=cred['host'],user=cred['username'],pwd=cred['password'],cmd=cmd)
        else : 
            cmdn=f'ls /logs01/SCM/backup/ | grep {dtstring1} | wc -l'
            ndata=SshNode(host=cred['host'],user=cred['username'],pwd=cred['password'],cmd=cmdn)
            n=str(ndata.decode('ascii')).replace('\n','')
            if int(n) > 0 :
                cmd=f"zgrep -ah {trxid} /logs01/SCM/backup/*{dtstring1}*" 
                data=SshNode(host=cred['host'],user=cred['username'],pwd=cred['password'],cmd=cmd)
            else :
                txtfinal=f'log file {dtstr} not available on log server'
        try :
            raw_data=data.decode('ascii').split("\n")
            data_clean=[]
            if raw_data :
                for d in raw_data :
                    if d is not None or d !=  '' :
                        data_clean.append(d)
                txtfinal='\n'.join(data_clean)
        except Exception :
            pass
        os.system("clear")
        os.system("clear")
        print (f'{grs}\n\t\t\t\t\t\tSCM LOG - {trxid}\n{grs}\n\n{txtfinal}\n\n{grs}')
    else :
        os.system("clear")
        os.system("clear")
        print (f'{grs}\n\t\t\t\tPlease check your input !!!!!\n{grs}')


#ESME LOG
def EsmeLog():
    temp=input('Fill MSISDN               : ')
    dtstr=input('Fill date (dd-mm-yyyy)    : ')
    td=GetToday()
    dt=ConvertStrtoDate(dtstr,'%d-%m-%Y')
    cred=ReadJsonFile(sdplogs)
    txtfinal=""
    if temp is not None and dtstr is not None : 
        if temp[0] == '0' :
            msisdn=f'62{temp[1:]}'
        else :
            msisdn=temp
        dtstring1=ConvertDatetoStr(dt,'%Y-%m-%d')
        print(f"login {cred['host']} ...")
        if dt.date() == td.date() : #today
            cmd=f'grep -ah {msisdn} /logs01/ESME/*{dtstring1}* | grep "DELIVER_SM(DeliverSm) \|DELIVERY_RECEIPT(DeliverSm)\|INFO  imp.bo.SynchSubmitSmBO:" | grep "destinationAddress\|ClientTransactionId"'
            data=SshNode(host=cred['host'],user=cred['username'],pwd=cred['password'],cmd=cmd)
        else :
            cmdn=f'ls /logs01/ESME/backup/ | grep {dtstring1} | wc -l'
            ndata=SshNode(host=cred['host'],user=cred['username'],pwd=cred['password'],cmd=cmdn)
            n=str(ndata.decode('ascii')).replace('\n','')
            if int(n) > 0 :
                cmd=f'zgrep -ah {msisdn} /logs01/ESME/*{dtstring1}* | grep "DELIVER_SM(DeliverSm) \|DELIVERY_RECEIPT(DeliverSm)\|INFO  imp.bo.SynchSubmitSmBO:" | grep "destinationAddress\|ClientTransactionId"'
                data=SshNode(host=cred['host'],user=cred['username'],pwd=cred['password'],cmd=cmd)
            else :
                txtfinal=f'log file {dtstr} not available on log server'
        try :
            raw_data=data.decode('ascii').split("\n")
            data_clean=[]
            if raw_data :
                for d in raw_data :
                    if d is not None or d !=  '' :
                        data_clean.append(d)
                txtfinal='\n'.join(data_clean)
        except Exception :
            pass
        os.system("clear")
        os.system("clear")
        print (f'{grs}\n\t\t\t\t\t\tESME LOG - {msisdn}\n{grs}\n\n{txtfinal}\n\n{grs}')
    else :
        os.system("clear")
        os.system("clear")
        print (f'{grs}\n\t\t\t\tPlease check your input !!!!!\n{grs}')
    