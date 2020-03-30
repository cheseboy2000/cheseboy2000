# -- coding: utf-8 --
from git import Repo
from git import Git
repo = Repo(r'D:/htdocs/online-crm')
# 获取默认版本库 origin
remote = repo.remote()
# 从远程版本库拉取分支
remote.pull()

r = Git("D:/htdocs/online-crm")
r.execute('git pull') 
print(r.execute('git pull'))
