import json
import os
import paramiko
import base64
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime,timedelta
from art import *
import plotext as plt


basedir=os.path.abspath(os.path.dirname(__file__))


def ReadTxtFile(pathfile):
    with open(pathfile,'r') as f:
        data=f.read()
    return data

def ReadJsonFile(pathfile):
    with open(pathfile,'r') as f:
        data=json.load(f)
    return data


def ConvertStrtoDate(tgl,format):
    dt=datetime.strptime(tgl,format)
    return dt

def ConvertDatetoStr(tgl,format):
    dt=datetime.strftime(tgl,format)
    return dt

def GetToday():
    dt=datetime.now()
    return dt


def SshNode(host=None,user=None,pwd=None,cmd=None):
    client =paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host,username=user,password=pwd)
    stdin,stdout,stderr=client.exec_command(cmd)
    return stdout,stderr
    client.close()


def Banner(text=None):
    string=text
    tprint (string,space=1)


def EncryptToBase64(text=None):
    if text is not None :
        txtbase64=base64.b64encode(text.encode('utf-8')).decode('utf-8')
        return txtbase64
    return None


def EncryptAES(text=None,key=None):
    if text is not None and key is not None :
        cipher = AES.new(key.encode("utf8"), AES.MODE_ECB)
        ct_bytes = cipher.encrypt(pad(text.encode("utf8"), AES.block_size))
        ct = b64encode(ct_bytes).decode('utf-8')
        return ct
    return None


def BarChart(x=None,y=None,title=None):
    if x is not None and y is not None :
        plt.bar(x, y)
        plt.ylim(0, 38)
        plt.plotsize(100, 20)
        plt.title(title)
        plt.show()
 
        
def PrintScpCdr(data=None):
    grs='-'*47
    d=data
    starttime=f"{str(d['CALL_START_TIME'])[:4]}-{str(d['CALL_START_TIME'])[4:6]}-{str(d['CALL_START_TIME'])[6:8]} {str(d['CALL_START_TIME'])[8:10]}:{str(d['CALL_START_TIME'])[10:12]}:{str(d['CALL_START_TIME'])[12:]}"
    stoptime=f"{str(d['CALL_DISCONNECTING_TIME'])[:4]}-{str(d['CALL_DISCONNECTING_TIME'])[4:6]}-{str(d['CALL_DISCONNECTING_TIME'])[6:8]} {str(d['CALL_DISCONNECTING_TIME'])[8:10]}:{str(d['CALL_DISCONNECTING_TIME'])[10:12]}:{str(d['CALL_DISCONNECTING_TIME'])[12:]}"
    txt=f"""{grs} {d['TRANSACTION_ID']} {grs}
************* IDP RECEIVED *************
CDR DATE  : {d['CDR_DATE']}
CDR TIME    : {d['CDR_HOUR']}
CALL REF    : {d['CALL_REFERENCE_NUMBER']}
A_NUMBER    : {d['CALLING_PARTY']}
B_NUMBER    : {d['CALLED_PARTY']}
SERVICE KEY : {d['SERVICE_KEY']}
CELL ID     : {d['CELL_ID']}
MSC ADDR    : {d['MSC_ADDRESS']}
VLR ADDR    : {d['VLR_ADDRESS']}
CALL TYPE   : {d['CALL_TYPE']} 

************* NORM & DENORM *************   
NORM   : {d['NORMALISED_NUMBER']}
DENORM : {d['TRANSLATED_NUMBER']}

************* OCS *************
DIAMETER  ERROR CODE : {d['DIAMETER_RESULT_CODES']} - {d['DIAMETER_ERROR_MESSAGE']}
DIAMETER SESSION     : {d['DIAMTER_SESSION_ID']}
CALL DURATION        : {d['CALL_DURATION']} ( start : {starttime} ,stop : {stoptime} )
CALL STATUS          : {d['CALL_STATUS']}

************* OTHERS INFO   *************
TRANSACTION ID : {d['TRANSACTION_ID']}
SUB CALL TYPE  : {d['SUB_CALL_TYPE']}
SUBSCRIBER TYPE: {d['SUBSCRIBER_TYPE']}
ROAMING        : {d['IS_ROAMING']}
BFT            : {d['ISBFT']}
FOC            : {d['IS_FOC']}
INSTANCE ID    : {d['INSTANCE_ID']}
{grs}{grs}\n"""
    print (txt)
    
    
def SshNode(host=None,user=None,pwd=None,cmd=None):
    client =paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host,username=user,password=pwd)
    stdin,stdout,stderr=client.exec_command(cmd)
    return stdout.read()
    client.close()
