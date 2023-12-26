import pandas as pd
import os
import json
from datetime import datetime,timedelta
from Modules.general import ReadJsonFile,ReadTxtFile,SshNode,ConvertStrtoDate,ConvertDatetoStr
from Modules.readconfig import AllConfig
from find_log import ScmLog,SdpSV,EsmeLog,ScpLog


trxid='821152923'
dtstr='12-12-2023'
scplogcred='/home/scpsdpdev/clitool/Scripts/Connection/scplog.json'
dt=ConvertStrtoDate(dtstr,'%d-%m-%Y')
cred=ReadJsonFile(scplogcred)
c=cred[0]
print(f"login {c['host']} ...")
dtstring1=ConvertDatetoStr(dt,'%Y%m%d')
dtstring2=ConvertDatetoStr(dt,'%Y-%m-%d')
cmd=f'grep -ah {trxid} /opt/logs/scp_app/*{dtstring1}*;zgrep -ah {trxid} /opt/logs/scp_app/*{dtstring2}*'
datatemp=SshNode(host=c['host'],user=c['username'],pwd=c['password'],cmd=cmd)       
dataraw=[]
data=datatemp.decode('ascii').split('\n')
for d in data :
    dataraw.append(d)
data_clean=[]
if dataraw :
    for d in dataraw :
        if d is not None or d !=  '' :
            try :
                djson=json.loads(d)
                txt=f"{djson['logData']['data']['TimeStamp']} - {djson['logData']['data']['EventTID']} - {djson['logData']['data']['EventType']} - {djson['logData']['data']['EventCategory']} : {djson['logData']['data']['EventMessage']}"
                print(txt)
                data_clean.append(djson)
            except Exception :
                pass
#print(data_clean)