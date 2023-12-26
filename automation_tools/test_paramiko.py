# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 16:01:48 2023

@author: HS00935501
"""

import os
import pandas as pd
#import base64
import json
import paramiko
#from datetime import datetime, timedelta,time
#from Modules.general import ReadJsonFile,ReadTxtFile,ConvertStrtoDate,ConvertDatetoStr,BarChart,PrintScpCdr
#from Modules.readconfig import ConfigScm,AllConfig


def SshNode(host=None,user=None,pwd=None,cmd=None):
    client =paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host,username=user,password=pwd)
    stdin,stdout,stderr=client.exec_command(cmd)
    return stdout.read().decode()
    client.close()

filejson='/home/scpsdpdev/clitool/Scripts/Connection/sdplog.json'


with open(filejson,'r') as f :
    data=json.load(f)

cred=data

print(cred)
data=SshNode(host=cred['host'],user=cred['username'],pwd=cred['password'],cmd='df -h ')
print(data)

"""
list_raw=[]
for d in data:
    #cmd='ls /opt/logs/scp_app/*2023-11-26* | wc -l'
    cmd='zgrep -ah 809772886 /opt/logs/scp_app/*20231127*'
    data=SshNode(host=d['host'],user=d['username'],pwd=d['password'],cmd=cmd)
    #tmp=int(data.replace('\n',''))
    list_raw.append(data)
print(list_raw)"""