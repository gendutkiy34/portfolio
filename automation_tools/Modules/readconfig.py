import os
import time
import pandas as pd
from Modules.connection import OracleConPd
from Modules.general import ReadJsonFile,GetToday


class ConfigScm():

    def __init__(self,connectionpath=None,cpid=None,):
        self.cred=ReadJsonFile(pathfile=connectionpath)
        self.strconn=None
        self.flagcon=0
        self.cpid=cpid
        self.strconn=f'{self.cred["username"]}/{self.cred["password"]}@{self.cred["host"]}:{self.cred["port"]}/{self.cred["sid"]}'
        if self.cpid is not None and self.strconn is not None:
            self.flagcon=1
        elif self.cpid is None and self.strconn is not None:
            self.flagcon=1
        else :
            self.flagcon=0

    def VerifyConn(self):
        print (self.strconn)

    def QueryConf(self,sqltext=None):
        list_column=[]
        list_raw=[]
        if self.flagcon == 1 :
            if self.cpid is not None :
                cmdsql=sqltext.format(string_connection=self.strconn,cpid=self.cpid)
                raw=os.popen(cmdsql)
                for t in raw:
                    if 'rows selected' in t or 'spooling'in t :
                        pass
                    else :
                        tempt=t.replace('"','').replace('\n','')
                        if 'CP_ID' in tempt :
                            temp=tempt.split('|')
                            list_column=temp
                        elif tempt is not None :
                            temp=tempt.split('|')
                            list_raw.append(temp)
                        else :
                            pass
                df=pd.DataFrame(list_raw,columns=list_column)
                return df
        else :
            return None
        
class AllConfig():

    def __init__(self,connectionpath=None):
        self.cred=ReadJsonFile(pathfile=connectionpath)
        self.strconn=None
        self.flagcon=0
        self.strconn=f'{self.cred["username"]}/{self.cred["password"]}@{self.cred["host"]}:{self.cred["port"]}/{self.cred["sid"]}'
        if self.strconn is not None :
            self.flagcon=1

    def VerifyConn(self):
        return self.strconn

    def Verifyflag(self):
        print (self.flagcon)

    def Queryall(self,sqltext=None):
        if self.flagcon == 1 :
            i=0
            list_column=[]
            list_raw=[]
            raw=os.popen(sqltext)
            try :
                for t in raw:
                    if 'rows selected' in t or 'spooling'in t :
                        pass
                    else :
                        temp=t.replace('"','').replace('\n','')
                        tempslit=temp.split('|')
                        if len(tempslit) > 1 :
                            if isinstance(tempslit,list) and i ==1:
                                [list_column.append(c) for c in tempslit ]
                            else :
                                list_raw.append(tempslit)
                    i += 1
                df=pd.DataFrame(list_raw,columns=list_column)
                dictdf=df.to_dict('records')
                return dictdf
            except Exception :
                return None
        else :
            return None




















