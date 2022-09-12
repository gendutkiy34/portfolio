'''
This Class Function to make easy git operation in python script
'''

from git import Repo
import git
import os
import re
import json

class GitRepo():
  
  def __init__(self,local_repository):
    self.local_repos=local_repository
    
  def GitClone(self,url):
    try :
      git.Repo.clone_from(url,self.local_repos)
      print('Remote Repository cloned !!!')
    except Exception as e :
      raise e
      
  def GitInit(self):
    repository=Repo.init(self.local_repos)
    return repository
  
  def GitStatus(self):
    repository=git.Repo(self.local_repos)
    status=repository.git.status()
    print(status)
    
  def GitFetch(self):
    repository=git.Repo(self.local_repos)
    repo.remote().fetch()
    for fl in os.listdir(self.local_repos):
      print(fl)
      
  def GitAdd(self,filename=None,message_commit):
    repository=git.Repo(self.local_repos)
    if filename == None :
      repository.git.add('--all')
    else :
      repository.git.add(filename)
    repository.git.commit('-m',message_commit)
    GitStatus()
    
  def GitPush(self,filename=None,message_commit):
    repository=git.Repo(self.local_repos)
    origin = repository.remote(name='origin')
    origin.push()
    print("push success !!")
    
  def GitLog(self):
    repository=git.Repo(self.local_repos)
    temp=repository.git.log()
    log=temp.split('\n')
    for txt in log:
        print(txt)
        
  def GitPull(self):
    repository=git.Repo(self.local_repos)
    origin = repo.remote(name='origin')
    origin.pull()
    for fl in os.listdir(self.local_repos):
      print(fl)