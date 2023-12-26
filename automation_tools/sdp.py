# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 19:01:45 2023

@author: HS00935501
"""
import os
import pandas as pd 
from sdp_config import CpCon,SubsOffer,CpSdc,Encode64,BolehNet,SubKeyword,EncryptMsisdn, \
     EncodeAes,WapUrl,EncryptMsisdn2,DecryptMsisdn2,Subcription
from sdp_trx import CdrTrx
from find_log import ScmLog,SdpSV,EsmeLog
from Modules.general import Banner

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
1.  SDP - CDR PROD                               11. SDP - Generate Wap URL
2.  SDP - CDR SIT                                12. SDP - MSISDN to ENCRYPTION
3.  SDP - CP CONNECTION                          13. SDP - GET DATA SUBSCRIPTION
4.  SDP - CP OFFER CODE                          14. LOG - SCM 
5.  SDP - SDC                                    15. LOG - ESME 
6.  SDP - ENCRYPT TO BASE64                      16. LOG - BILLING
7.  SDP - CHECK CONTENT BOLEH NET
8.  SDP - CHECK  SUB KEYWORD
9.  SDP - ENCRYPTION to MSISDN
10. SDP - ENCRYPT TO AES
Please choose one : 
"""
opt=input(head)

if opt == "1":
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tCHECK CDR SDP\n{grs2}"
    Banner(textbanner)
    print(info)
    CdrTrx()      
elif opt == "2":
    pass
elif opt == "3" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tCHECK CONFIGURATION CP CONNECTION\n{grs2}"
    Banner(textbanner)
    print(info)
    CpCon()
elif opt == "4" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tCHECK CONFIGURATION OFFER CODE\n{grs2}"
    Banner(textbanner)
    print(info)
    SubsOffer()
elif opt == "5" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tCHECK CONFIGURATION CP SDC\n{grs2}"
    Banner(textbanner)
    print(info)
    CpSdc()
elif opt == "6" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tCONVERT STRING TO BASE64\n{grs2}"
    Banner(textbanner)
    print(info)
    Encode64()
elif opt == "7" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tCHECK CONTENT BOLEH NET\n{grs2}"
    Banner(textbanner)
    print(info)
    BolehNet()
elif opt == "8" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tCHECK SUB KEYWORD\n{grs2}"
    Banner(textbanner)
    print(info)
    SubKeyword()
elif opt == "9" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tENCRYPTION to MSISDN\n{grs2}"
    Banner(textbanner)
    print(info)
    EncryptMsisdn2()
elif opt == "10" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tENCRYPT to AES\n{grs2}"
    Banner(textbanner)
    print(info)
    EncodeAes()
elif opt == "11" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tGENERATE WAP URL\n{grs2}"
    Banner(textbanner)
    print(info)
    WapUrl()
elif opt == "12" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tMSISDN to ENCRYPTION\n{grs2}"
    Banner(textbanner)
    print(info)
    DecryptMsisdn2()
elif opt == "13" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tCHECK SUBSCRIPTION\n{grs2}"
    Banner(textbanner)
    print(info)
    Subcription()
elif opt == "14" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tFIND LOG SCM\n{grs2}"
    Banner(textbanner)
    print(info)
    ScmLog()
elif opt == "15" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tFIND LOG ESME\n{grs2}"
    Banner(textbanner)
    print(info)
    EsmeLog()
elif opt == "16" :
    os.system('clear')
    info=f"{grs2}\n\n\t\t\t\t\t\tFIND LOG BILLING\n{grs2}"
    Banner(textbanner)
    print(info)
    SdpSV()
else :
    print ('WRONG INPUT !!!')