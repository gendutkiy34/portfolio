import os
import pandas as pd
import base64
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime, timedelta,time
from Modules.general import GetToday,ReadJsonFile,ReadTxtFile,ConvertStrtoDate,ConvertDatetoStr,EncryptToBase64,EncryptAES
from Modules.readconfig import ConfigScm,AllConfig

pd.set_option('display.max_rows', None)
basedir=os.path.abspath(os.path.dirname(__file__))

scmusr=f'{basedir}/Connection/sdp_scm_mm.json'
comads=f'{basedir}/Connection/sdp_comads.json'
morusr=f'{basedir}/Connection/sdp_mm_mor.json'
txtnotfound='\t\t\tDATA NOT FOUND !!!'
grs='-'*45  
grs2='='*45


#CP CONNECTION
def CpCon():
    CpId=input('Masukkan CP ID : ')
    sqltxt=f'{basedir}/sql/cpconnection.sql'
    sql=ReadTxtFile(pathfile=sqltxt)
    consdp=ConfigScm(connectionpath=scmusr,cpid=CpId)
    dfcpcon=consdp.QueryConf(sqltext=sql)
    dffilter=dfcpcon[dfcpcon['CP_ID']==str(CpId)]
    dfdispl=dffilter[['CP_ID','NAME', 'OFFER_CODE', 'CONNECTION_NAME', 'CONNECTION_TYPE', 'SYSTEM_ID', 'PASSWORD', 'SUBSCRIPTION_TYPE', 'STATUS']]
    os.system('clear')
    os.system('clear')
    print(f'{grs2}{grs2}{grs2}\n{dfdispl}\n{grs2}{grs2}{grs2}\n\n')
    offcode=input("fill offer code for detail\n(use ';' as delimeter for more than one ) : ")
    print('\n')
    list_ofcode=offcode.split(';')
    dftemp=dffilter[dffilter['OFFER_CODE'].isin(list_ofcode)]
    if len(dftemp.index) > 0:
        dictoffercode=dftemp.to_dict('records')
        for d in dictoffercode:
            txt=f"""{grs} {d['OFFER_CODE']} {grs}
CP NAME\t\t: {d['NAME']}
OFFER CODE\t: {d['OFFER_CODE']}
CON NAME\t: {d['CONNECTION_NAME']}
CON TYPE\t: {d['CONNECTION_TYPE']}
SYSTEM ID\t: {d['SYSTEM_ID']}
PASSWORD\t: {d['PASSWORD']}
SUBS TYPE\t: {d['SUBSCRIPTION_TYPE']}
STATUS\t\t: {d['STATUS']}
BIND TYPE\t: {d['BIND_TYPE']}
CONCURRENT\t: {d['MAX_CONCURRENT_CONNECTION']}
TPS\t\t: {d['TPS']}
BUFFER\t\t: {d['BUFFER']}
MO TYPE\t\t: {d['MO_DR_TYPE']}
MO URL\t\t: {d['MO_URL_1']}
DR URL\t\t: {d['DR_URL1']}
{grs}{grs}\n
"""
            print (txt)
    else :
        print (f'{grs}{grs}\n\t\t\t\tDATA NOT FOUND !!!!!\n{grs}{grs}')



#CP OFFER
def SubsOffer():
    head="""1. cp id
2. offer code
Please choose one : \n"""
    opt=input(head)
    if opt == "1" :
        CpId=input('Masukkan CP ID : ')
        cond=f"WHERE CP_ID='{CpId}'"
        #pdcond=dfoffer['CP_ID']==str(CpId)
        flag=1
    elif opt == "2" :
        offcode=input('Masukkan Offer Code : ')
        cond=f"WHERE OFFER_CODE='{offcode}'"  
        #pdcond=dfoffer['OFFER_CODE']==str(offcode)  
        flag=1
    else :
        flag=0
    if flag == 1 :
        sqltxt=f'{basedir}/sql/offercode.sql'
        sql=ReadTxtFile(pathfile=sqltxt)
        consdp=AllConfig(connectionpath=scmusr)
        sqlfull=sql.format(condition=cond,string_connection=consdp.VerifyConn())
        dictoffer=consdp.Queryall(sqltext=sqlfull)
        if dictoffer is not None :
            dfoffer=pd.DataFrame(dictoffer)
            dfdispl=dfoffer[['CP_ID','CP_NAME', 'OFFER_CODE', 'OFFER_DESC','SHORT_CODE', 'SUBSCRIPTION_MODE','AUTO_RENEWAL_MAX_SPAN', 'STATUS','CREATE_DATE']]
            os.system('clear')
            os.system('clear')
            print(f'{grs2}{grs2}{grs2}\n{dfdispl}\n{grs2}{grs2}{grs2}\n\n')
            offcode=input("fill offer code for detail\n(use ';' as delimeter for more than one ) : ")
            print('\n')
            list_ofcode=offcode.split(';')
            dftemp=dfoffer[dfoffer['OFFER_CODE'].isin(list_ofcode)]
            if len(dftemp.index) > 0:
                dictoffercode=dftemp.to_dict('records')
                for d in dictoffercode:
                    txt=f"""{grs} {d['OFFER_CODE']} {grs}
CP NAME\t\t: {d['CP_NAME']}
OFFER CODE\t: {d['OFFER_CODE']}
OFFER NAME\t: {d['OFFER_NAME']}
OFFER DESC\t: {d['OFFER_DESC']}
SHORT CODE\t: {d['SHORT_CODE']}
SUBS MODE\t: {d['SUBSCRIPTION_MODE']}
MAX SPAN\t: {d['AUTO_RENEWAL_MAX_SPAN']}
STATUS\t\t: {d['STATUS']}
CHANNELID\t: {d['CHANNEL_ID']}
DEACT RULE\t: {d['AUTO_DEACTIVATION_RULE']}
CP NOTIFICATION\t: {d['CP_NOTIFICATION']}
KEYWORD\t\t: {d['KEYWORD']}
CREATE DATE\t: {d['CREATE_DATE']}
UPDATE DATE\t: {d['UPDATE_DATE']}
CODE ARG\t: {d['CODE_ARGUMENT']}
{grs}{grs}\n
"""
                    print (txt)
            else :
                print (f'{grs}{grs}\n\t\t\t\tDATA NOT FOUND !!!!!\n{grs}{grs}')
        else :
          print (f'{grs}{grs}\n\t\t\t\tDATA NOT FOUND !!!!!\n{grs}{grs}')  
    else :
        print (f'{grs}{grs}\n\t\t\t\tDATA NOT FOUND !!!!!\n{grs}{grs}')


#CP SDC
def CpSdc():
    head="""1. CP ID
2. Offer Code
3. SDC
Please choose one : \n"""
    opt=input(head)
    if opt == "1" :
        CpId=input('Please fill CP ID : ')
        cond=f"WHERE b.CP_ID='{CpId}'"
        flag=1
    elif opt == "2":
        OffCd=input('Fill Offer Code : ')
        cond=f"WHERE a.OFFER_ID='{OffCd}'"
        flag=1
    elif opt == "3" :
        Sdc=input('Please fill MO Shortcode : ')
        cond=f"WHERE a.MO_SHORT_CODE ='{Sdc}'"
        flag=1
    else :
        flag=0
    if flag == 1:
        sqltxt=f'{basedir}/sql/sdc.sql'
        sql=ReadTxtFile(pathfile=sqltxt)
        consdp=AllConfig(connectionpath=scmusr)
        sql=ReadTxtFile(pathfile=sqltxt)
        sqlfull=sql.format(condition=cond,string_connection=consdp.VerifyConn())
        dictsdc=consdp.Queryall(sqltext=sqlfull)
        if dictsdc:
            dfsdc=pd.DataFrame(dictsdc)
            dfdispl=dfsdc[['CP_NAME', 'OFFER_CODE', 'MO_SHORT_CODE','SENDER_MASKING_ADDRESS', 'TYPE_OF_DIRECTION','CHARGE_AMOUNT', 'CREATE_DATE' ]]
            os.system('clear')
            os.system('clear')
            print(f'{grs2}{grs2}{grs2}\n{dfdispl}\n{grs2}{grs2}{grs2}\n\n')
        else :
            os.system('clear')
            os.system('clear')
            print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')
    else :
        os.system('clear')
        os.system('clear')
        print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')


#CONTENT BOLEH NET
def BolehNet():
    grs='-'*30  
    grs2='='*30
    MonYear=input('Enter mon and year (mm-yyyy): ')
    dt=ConvertStrtoDate(MonYear,'%m-%Y')
    dtstring=ConvertDatetoStr(dt,'%B %Y')
    sqltxt=f'{basedir}/sql/bolehnet.sql'
    sql=ReadTxtFile(pathfile=sqltxt)
    consdp=AllConfig(connectionpath=comads)
    sqlfull=sql.format(monyear=MonYear,string_connection=consdp.VerifyConn())
    dictcontent=consdp.Queryall(sqltext=sqlfull)
    if len(dictcontent):
        for d in dictcontent:
            if 'daily' in str(d['CONTENT_NAME']).lower() :
                d['SUBS_TYPE']='daily'
            elif 'weekly' in str(d['CONTENT_NAME']).lower() :
                d['SUBS_TYPE']='weekly'
            elif 'monthly' in str(d['CONTENT_NAME']).lower() :
                d['SUBS_TYPE']='monthly'
            elif 'on demand' in str(d['CONTENT_NAME']).lower() :
                d['SUBS_TYPE']='on demand'
            else :
                d['SUBS_TYPE']='pay in advance'
            if 'chinese horoscope' in str(d['CONTENT_NAME']).lower() :
                d['CATEGORY']='chinese horoscope'
            elif 'ramalan cinta' in str(d['CONTENT_NAME']).lower() :
                d['CATEGORY']='ramalan cinta'
            elif 'iod horoscope' in str(d['CONTENT_NAME']).lower() :
                d['CATEGORY']='iod horoscope'
            elif 'comedy' in str(d['CONTENT_NAME']).lower() :
                d['CATEGORY']='comedy'
            else :
                d['CATEGORY']='others'
        dfall=pd.DataFrame(dictcontent)
        dfsum=dfall[['CONTENT_PREFIX','SERVICE_NAME','CATEGORY','SUBS_TYPE']].groupby(['SERVICE_NAME','CATEGORY','SUBS_TYPE']).size().reset_index(name='TOTAL')
        list_sub=['daily','weekly','monthly','on demand','pay in advance']
        dictsum={}
        for s in list_sub:
            dftemp=dfsum[dfsum['SUBS_TYPE']==s]
            sumtemp=dftemp.groupby(['CATEGORY','SUBS_TYPE'])['TOTAL'].sum().reset_index(name='TOTAL')
            dictsum[s]=sumtemp.to_dict('records')
        summall=dfsum.groupby(['SUBS_TYPE'])['TOTAL'].sum().reset_index(name='TOTAL')
        dictsum['summary']=summall.to_dict('records')
        txt=f'''{grs2}{grs2}
\tCONTENT BOLEH NET - {dtstring}
{grs2}{grs2}
{pd.DataFrame(dictsum["daily"])}
{grs}{grs}
{pd.DataFrame(dictsum["weekly"])}
{grs}{grs}
{pd.DataFrame(dictsum["monthly"])}
{grs}{grs}
{pd.DataFrame(dictsum["on demand"])}
{grs}{grs}
{pd.DataFrame(dictsum["pay in advance"])}
{grs}{grs}

{grs2}{grs2}
\t\tSUMMARY - {dtstring}
{grs2}{grs2}
{pd.DataFrame(dictsum["summary"])}
{grs}{grs}'''
        os.system('clear')
        os.system('clear')
        print(txt)
    else :
        os.system('clear')
        os.system('clear')
        print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')


def Encode64():
    flag=1
    while flag==1 :
        strinput=input('Fill string fo convert base64 : \n')
        try :
            txtbase64=base64.b64encode(strinput.encode('utf-8')).decode('utf-8')
            print(txtbase64)
            opt=input("\ndo you try another input ? (Y/N) : ")
            if opt.upper() == 'Y' :
                flag=1 
            else :
                flag=0
        except Exception :
            pass

def SubKeyword():
    grs='-'*30  
    grs2='='*30
    head="""1. keyword
2. Offer Code
Please choose one : \n"""
    opt=input(head)
    if opt == "1" :
        tempkey=input('Please input keyword : ')
        cond=f"WHERE KEYWORD like '%{tempkey.upper()}%'"
        flag=1
    elif opt == "2" :
        ofcode=input('Please input offer code : ')
        cond=f"WHERE KEY_VALUES='{ofcode}'"
        flag=1
    else :
        flag=0
    if flag == 1 :
        sqltxt=f'{basedir}/sql/subkeyword.sql'
        sql=ReadTxtFile(pathfile=sqltxt)
        consdp=AllConfig(connectionpath=morusr)
        sqlfull=sql.format(condition=cond,string_connection=consdp.VerifyConn())
        dictsubkeyword=consdp.Queryall(sqltext=sqlfull)
        if dictsubkeyword is not None :
            if len(dictsubkeyword) != 0 :
                dfsubkey=pd.DataFrame(dictsubkeyword)
                os.system('clear')
                os.system('clear')
                print(f'{grs2}{grs2}{grs2}\n{dfsubkey}\n{grs2}{grs2}{grs2}\n\n')
            else :
                os.system('clear')
                os.system('clear')
                print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')
    else :
        pass


def EncryptMsisdn():
    grs='-'*30  
    grs2='='*30
    head="""1. input manual
2. Batch ( from file )
Please choose one : \n"""
    opt=input(head)
    if opt == "1" :
        head2="""Please input encryption 
(please use ';' as separtor for input more than 1) : """
        tempencrypt=input(head2)
        templist=tempencrypt.split(';')
        if len(templist) != 1 :
            listencrypt=("','").join(templist)
        else :
            listencrypt=templist[0]
        flag=1
    elif opt == "2" :
        pathfile=input('please input path  & filename : ')
        with open(pathfile,'r') as f :
            data=f.readlines()
        list_data=[t.replace('\n','').replace('\r','') for t in data ]
        listencrypt=("','").join(list_data)
        flag=1
    else :
        flag=0
    if flag  == 1 :
        sqltxt=f'{basedir}/sql/encryption_msisdn.sql'
        sql=ReadTxtFile(pathfile=sqltxt)
        consdp=AllConfig(connectionpath=scmusr)
        sqlfull=sql.format(encryption=listencrypt,string_connection=consdp.VerifyConn())
        print(sqlfull)
        dictencrypt=consdp.Queryall(sqltext=sqlfull)
        if dictencrypt is not None :
            if len(dictencrypt) != 0 :
                dfencryp=pd.DataFrame(dictencrypt)
                os.system('clear')
                os.system('clear')
                print(f'{grs2}{grs2}\n{dfencryp}\n  {grs2}{grs2}\n\n')
            else :
                os.system('clear')
                os.system('clear')
                print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')
    else :
        pass
    

def EncodeAes():
    flag=1
    while flag==1 :
        strinput=input('please input string fo convert AES : \n')
        keyinput=input('please input key: \n')
        try :
            cipher = AES.new(keyinput.encode("utf8"), AES.MODE_ECB)
            ct_bytes = cipher.encrypt(pad(strinput.encode("utf8"), AES.block_size))
            ct = b64encode(ct_bytes).decode('utf-8')
            print(ct)
            opt=input("\ndo you try another input ? (Y/N) : ")
            if opt.upper() == 'Y' :
                flag=1 
            else :
                flag=0
        except Exception :
            pass


def WapUrl():
    Secret_Key='@tW1Un5e6(@$#a7)'
    head="""1. Manual
2. Massive (file)
Please choose one :\n"""
    opt=input(head)
    if opt == '1' :
        offcode=input('Please input offer code : ')
        cpid=input('Please input cp id : ')
        keyword=input('Please input keyword ( without REG ) : ')
        txt_offer=f'{offcode}||REG {str(keyword).upper()}'
        offerb64=EncryptToBase64(text=txt_offer)
        cpb64=EncryptToBase64(text=f'QWRtaW46QWRtaW5AMTIz||{cpid}')
        urlaes=EncryptAES(text=cpb64,key=Secret_Key)
        urladdrs=f'http://wapsdp.tri.co.id/Redirect?payload={offerb64}&auth={urlaes}'
        print (f'\n\n{grs2}{grs2}\nWAP URL :\n\n{urladdrs}\n{grs2}{grs2}')
    elif opt == '2':
        head2="""Format file without header
cp_id;offer_code;keyword
ex :
2895;30040;IMOVEAPP1

please fill fullpathname textfile:\n"""
        filepath=input(head2)
        list_result=[]
        td=GetToday()
        dtstring=ConvertDatetoStr(td,'%Y%m%d%H%M')
        outputfile=f'/home/scpsdpdev/clitool/output/wapurl_{dtstring}.csv'
        try :
            with open(filepath,'r') as f:
                data=f.readlines()
            for d in data :
                item={}
                temp=d.replace('\n','').replace('\r','')
                txtsplit=temp.split(';')
                item['CP_ID']=txtsplit[0]
                item['OFFERCODE']=txtsplit[1]
                item['KEYWORD']=f'REG {str(txtsplit[2]).upper()}'
                txt_offer=f'{txtsplit[1]}||REG {str(txtsplit[2]).upper()}'
                offerb64=EncryptToBase64(text=txt_offer)
                cpb64=EncryptToBase64(text=f'QWRtaW46QWRtaW5AMTIz||{txtsplit[0]}')
                urlaes=EncryptAES(text=cpb64,key=Secret_Key)
                urladdrs=f'http://wapsdp.tri.co.id/Redirect?payload={offerb64}&auth={urlaes}'
                item['WAP_URL']=urladdrs
                list_result.append(item)
            dfwapurl=pd.DataFrame(list_result)
            dfwapurl.to_csv(outputfile,index=False)
            os.system('clear')
            os.system('clear')
            print(f'{grs2}{grs2}\ngenerate success , file :{outputfile}\n  {grs2}{grs2}\n\n')
        except Exception :
            print(f'{grs2}{grs2}\nGENERATE WAP URL FAILED, please check requirement !!\n  {grs2}{grs2}\n\n')
    else :
        pass

def EncryptMsisdn2():
    grs='-'*30  
    grs2='='*30
    head="""1. input manual
2. Batch ( from file )
Please choose one : \n"""
    opt=input(head)
    if opt == "1" :
        head2="""Please input encryption 
(please use ';' as separtor for input more than 1) : """
        tempencrypt=input(head2)
        templist=tempencrypt.split(';')
        if len(templist) != 1 :
            listencrypt=("','").join(templist)
        else :
            listencrypt=templist[0]
        flag=1
    elif opt == "2" :
        pathfile=input('please input path  & filename : ')
        with open(pathfile,'r') as f :
            data=f.readlines()
        list_data=[t.replace('\n','').replace('\r','') for t in data ]
        list_chunk = [list_data[i:i + 100] for i in range(0, len(list_data), 100)]
        flag=2
    else :
        flag=0
    sqltxt=f'{basedir}/sql/encryption_msisdn.sql'
    sql=ReadTxtFile(pathfile=sqltxt)
    consdp=AllConfig(connectionpath=scmusr)
    if flag  == 1 :
        sqlfull=sql.format(encryption=listencrypt,string_connection=consdp.VerifyConn())
        dictencrypt=consdp.Queryall(sqltext=sqlfull)
        if dictencrypt is not None :
            if len(dictencrypt) != 0 :
                dfencryp=pd.DataFrame(dictencrypt)
                os.system('clear')
                os.system('clear')
                print(f'{grs2}{grs2}\n{dfencryp}\n  {grs2}{grs2}\n\n')
            else :
                os.system('clear')
                os.system('clear')
                print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')
    elif flag  == 2 :
        i = 1
        list_raw=[]
        dt=GetToday()
        dt_string=dt.strftime('%Y%m%d')
        output_file=f'/home/scpsdpdev/clitool/output/msisdn_encryption_{dt_string}.csv'
        print(f'total {len(list_chunk)} parts')
        for ch in list_chunk:
            temp="','".join(ch)
            sqlfull=sql.format(encryption=temp,string_connection=consdp.VerifyConn())
            dictencrypt=consdp.Queryall(sqltext=sqlfull)
            [list_raw.append(r) for r in dictencrypt ]
            print (f"grep data part {i} done")
            i += 1
        df=pd.DataFrame(list_raw)
        df.to_csv(output_file,index=False)
        msg=f'Generate done, output file : {output_file}'
        os.system('clear')
        os.system('clear')
        print(f'{grs2}{grs2}{grs2}\n{msg}\n{grs2}{grs2}{grs2}\n\n')
        
    else :
        pass

def DecryptMsisdn2():
    grs='-'*30  
    grs2='='*30
    head="""1. input manual
2. Batch ( from file )
Please choose one : \n"""
    opt=input(head)
    if opt == "1" :
        head2="""Please input encryption 
(please use ';' as separtor for input more than 1) : """
        tempencrypt=input(head2)
        templist=tempencrypt.split(';')
        if len(templist) > 1 :
            listtemp=[]
            for d in templist:
                listtemp.append(d[2:])
            listencrypt=("','").join(listtemp)
        else :
            listencrypt=templist[0][2:]
        flag=1
    elif opt == "2" :
        pathfile=input('please input path  & filename : ')
        with open(pathfile,'r') as f :
            data=f.readlines()
        list_data=[t.replace('\n','').replace('\r','') for t in data ]
        list_data_clean=[]
        [list_data_clean.append(m[2:]) for m in list_data]
        list_chunk = [list_data_clean[i:i + 100] for i in range(0, len(list_data), 100)]
        flag=2
    else :
        flag=0
    sqltxt=f'{basedir}/sql/decryption_msisdn.sql'
    sql=ReadTxtFile(pathfile=sqltxt)
    consdp=AllConfig(connectionpath=scmusr)
    if flag  == 1 :
        sqlfull=sql.format(decryption=listencrypt,string_connection=consdp.VerifyConn())
        dictencrypt=consdp.Queryall(sqltext=sqlfull)
        if dictencrypt is not None :
            if len(dictencrypt) != 0 :
                dfencryp=pd.DataFrame(dictencrypt)
                os.system('clear')
                os.system('clear')
                print(f'{grs2}{grs2}\n{dfencryp}\n  {grs2}{grs2}\n\n')
            else :
                os.system('clear')
                os.system('clear')
                print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')
                print(sqlfull)
    elif flag  == 2 :
        i = 1
        list_raw=[]
        dt=GetToday()
        dt_string=dt.strftime('%Y%m%d')
        output_file=f'/home/scpsdpdev/clitool/output/msisdn_decryption_{dt_string}.csv'
        print(f'total {len(list_chunk)} parts')
        for ch in list_chunk:
            temp="','".join(ch)
            sqlfull=sql.format(decryption=temp,string_connection=consdp.VerifyConn())
            dictencrypt=consdp.Queryall(sqltext=sqlfull)
            [list_raw.append(r) for r in dictencrypt ]
            print (f"grep data part {i} done")
            i += 1
        df=pd.DataFrame(list_raw)
        df.to_csv(output_file,index=False)
        msg=f'Generate done, output file : {output_file}'
        os.system('clear')
        os.system('clear')
        print(f'{grs2}{grs2}{grs2}\n{msg}\n{grs2}{grs2}{grs2}\n\n')
        
    else :
        pass


def Subcription():
    grs='-'*30  
    grs2='='*30
    cpid=input('Please input CP ID : ')
    head="""1. input manual
2. Batch ( from file )
Please choose one : \n"""
    opt=input(head)
    if opt == "1" :
        head2="""Please input msisdn 
(please use ';' as separtor for input more than 1) : """
        tempencrypt=input(head2)
        templist=tempencrypt.split(';')
        listtemp=[]
        if len(templist) > 1 :
            for d in templist:
                listtemp.append(d[2:])
            listmsisdn=("','").join(listtemp)
        else :
            listmsisdn=templist[0][2:]
        flag=1
    elif opt == "2" :
        pathfile=input('please input path  & filename : ')
        with open(pathfile,'r') as f :
            data=f.readlines()
        list_data=[t.replace('\n','').replace('\r','') for t in data ]
        list_data_clean=[]
        [list_data_clean.append(m[2:]) for m in list_data]
        list_chunk = [list_data_clean[i:i + 100] for i in range(0, len(list_data), 100)]
        flag=2
    else :
        flag=0
    sqltxt=f'{basedir}/sql/subscription.sql'
    sql=ReadTxtFile(pathfile=sqltxt)
    consdp=AllConfig(connectionpath=scmusr)
    dictencrypt=None
    if flag  == 1 :
        if cpid is not None or cpid != '':
            sqlfull=sql.format(cpid=cpid,msisdn=listmsisdn,string_connection=consdp.VerifyConn())
            dictencrypt=consdp.Queryall(sqltext=sqlfull)
            list_col_disp=['MSISDN','CP_ID','KEYWORD','STATUS', 'FREQUENCY', 'ACTIVATION_DATE','DEACTIVATION_DATE','NEXT_BILLING_DATE','LAST_CHARGE_DED_DATE']
            if dictencrypt is not None :
                if len(dictencrypt) != 0 :
                    dfencryp=pd.DataFrame(dictencrypt)
                    os.system('clear')
                    os.system('clear')
                    print(f'{grs2}{grs2}{grs2}{grs2}\n{dfencryp[list_col_disp]}\n{grs2}{grs2}{grs2}{grs2}\n\n')
            else :
                os.system('clear')
                os.system('clear')
                print(f'{grs2}{grs2}{grs2}\n{txtnotfound}\n{grs2}{grs2}{grs2}\n\n')
    elif flag  == 2 :
        if cpid is not None or cpid != '':
            i = 1
            list_raw=[]
            dt=GetToday()
            dt_string=dt.strftime('%Y%m%d')
            output_file=f'/home/scpsdpdev/clitool/output/subscription_{cpid}_{dt_string}.csv'
            print(f'total {len(list_chunk)} parts')
            for ch in list_chunk:
                temp="','".join(ch)
                sqlfull=sql.format(msisdn=temp,cpid=cpid,string_connection=consdp.VerifyConn())
                dictencrypt=consdp.Queryall(sqltext=sqlfull)
                [list_raw.append(r) for r in dictencrypt ]
                print (f"grep data part {i} done")
                i += 1
            df=pd.DataFrame(list_raw)
            df.to_csv(output_file,index=False)
            msg=f'Generate done, output file : {output_file}'
            os.system('clear')
            os.system('clear')
            print(f'{grs2}{grs2}{grs2}\n{msg}\n{grs2}{grs2}{grs2}\n\n')       
    else :
        pass
