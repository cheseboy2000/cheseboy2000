# -- coding: utf-8 --
from git import Repo
from git import Git
import time
import datetime
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class WallHandle:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        driver = webdriver.Chrome(options=options)
        self.driver=driver
    def getTheMonth(self,date, n):
        month = date.month
        year = date.year
        for i in range(n):
            if month == 1:
                year -= 1
                month = 12
            else:
                month -= 1
        return datetime.date(year, month, 1)
    def gitExe(self,dirStr,lines):
        r = Git(dirStr)
        lines=lines.split("\n")
        for index in lines:
            index=index.strip()
            if index!='' :
                if index.find("tag")==-1 :
                    print(index)
                try :
                    r.execute(index)
                except Exception :
                    print("异常")
                    return 
    def getLogDesc(self,dirStr):
        r = Git(dirStr)
        status=r.execute('git log -10')
        strs=status.split("\n")
        info =''

        for index in range(1,60,1):
            if strs[index].find(' ')!=0 :
                continue
            info=strs[index].replace(' ','')
            if info!='' and info.find("Merge") == -1  :
                break
        return info
    def viewHandle(self,tagname,num):
        driver=self.driver
        #60 线上 59 测试
        driver.get('http://walle.zhulong.dj:8484/筑龙学社/task/create/'+str(num))
        time.sleep(4)
        driver.find_elements_by_class_name("el-input__inner")[0].send_keys(tagname)
        driver.find_elements_by_class_name("el-button")[1].click()
        time.sleep(2)
        driver.get('http://walle.zhulong.dj:8484/筑龙学社/deploy/index')
        time.sleep(2)
        buttons=driver.find_elements_by_class_name("el-button--text")
        for i in buttons:
            if i.find_element_by_tag_name("span").text == "上线":
                i.click()
                break
        time.sleep(2)        
        driver.find_element_by_class_name("el-button--success").click()
        time.sleep(20)
    def gitpull(self):
        date = datetime.datetime.today()
        nowtime = date.strftime("%Y%m%d%H%M%S")
        lines='''git checkout master
        git fetch --all
        git pull --all
        git fetch origin develop:develop
        git merge develop
        git push
        git push  origin master
        '''
        self.gitExe("D:/htdocs/online-crm",lines)
        info=self.getLogDesc("D:/htdocs/online-crm")
        info=info.strip()
        info=info.replace('#','')
        info=info.replace('*','')
        tagname = '筑龙后台-'+nowtime+'-修改-'+info
        tagname=tagname.decode('utf8').encode('gb2312')
        lines='git tag '+tagname
        self.gitExe("D:/htdocs/online-crm",lines)
        lines='git push origin master tag '+tagname
        self.gitExe("D:/htdocs/online-crm",lines)
    def gitpullonline(self):
        date = datetime.datetime.today()
        nowtime = date.strftime("%Y%m%d%H%M%S")
        lines='''git checkout online
        git fetch --all
        git pull --all
        git fetch origin develop:develop
        git merge develop
        git push
        git push  origin online
        '''
        self.gitExe("D:/htdocs/online-crm",lines)
        info=self.getLogDesc("D:/htdocs/online-crm")
        info=info.strip()
        info=info.replace('#','')
        info=info.replace('*','')
        tagname = '筑龙后台-'+nowtime+'-修改-'+info
        tagname=tagname.decode('utf8').encode('gb2312')
        lines='git tag '+tagname
        self.gitExe("D:/htdocs/online-crm",lines)
        lines='git push origin master tag '+tagname
        self.gitExe("D:/htdocs/online-crm",lines)
    def handleExec(self,num):
        self.gitpull()
        self.publish(num)
    def publish(self,num):
        driver=self.driver
        driver.get('http://walle.zhulong.dj:8484/筑龙学社/task/create/'+str(num))
        time.sleep(5)
        inputs = driver.find_elements_by_tag_name("input")
        for i in inputs:
            if i.get_attribute("placeholder") == "选取Tag":
                if not i.is_enabled() :
                    self.publish(num)
                    return
                try :
                    i.click()
                    time.sleep(1)
                    el=driver.find_elements_by_class_name("el-select-dropdown__item")
                    text=el[0].find_element_by_tag_name("span").text
                    driver.find_elements_by_class_name("el-input__inner")[0].send_keys(text)
                    el[0].find_element_by_tag_name("span").click()
                except Exception :
                    try :
                        time.sleep(5)
                        i.click()
                        time.sleep(1)
                        el=driver.find_elements_by_class_name("el-select-dropdown__item")
                        text=el[0].find_element_by_tag_name("span").text
                        driver.find_elements_by_class_name("el-input__inner")[0].send_keys(text)
                        el[0].find_element_by_tag_name("span").click()
                    except Exception :
                        print("异常143")
                        return 
                break
        try :
            driver.find_elements_by_class_name("el-button")[1].click()
            time.sleep(2)
        except Exception :
            try :
                time.sleep(3)
                driver.find_elements_by_class_name("el-button")[1].click()
                time.sleep(2)
            except Exception :
                print("异常155")
                return 
        driver.get('http://walle.zhulong.dj:8484/筑龙学社/deploy/index')
        time.sleep(2)
        buttons=driver.find_elements_by_class_name("el-button--text")
        for i in buttons:
            if i.find_element_by_tag_name("span").text == "上线":
                try :
                    i.click()
                except Exception :
                    print("异常165")
                    return 
                break
        time.sleep(2)        
        driver.find_element_by_class_name("el-button--success").click()
        time.sleep(20)
    def tag(self):
        dirStr="D:/htdocs/online-crm"
        r = Git(dirStr)
        date = datetime.datetime.today()
        nowtime = date.strftime("%Y%m%d%H%M%S")
        info=self.getLogDesc("D:/htdocs/online-crm")
        info=info.strip()
        info=info.replace('#','')
        info=info.replace(':','')
        info=info.replace('*','')
        tagname = '筑龙后台-'+nowtime+'-修改-'+info
        tagname=tagname.decode('utf8').encode('gb2312')
        lines='git tag '+tagname
        print(lines.decode('gb2312').encode('utf8'))
        self.gitExe("D:/htdocs/online-crm",lines)
        lines='git push origin master tag '+tagname
        self.gitExe("D:/htdocs/online-crm",lines)
    def login(self):
        driver = self.driver
        driver.get('http://walle.zhulong.dj:8484/login')
        time.sleep(1)
        inputs = driver.find_elements_by_tag_name("input")
        for i in inputs:
            if i.get_attribute("type") == "text":
                i.send_keys('tanlei@zhulong.com')
            elif i.get_attribute("placeholder") == "请输入密码":
                i.send_keys('Zhulong123')
        driver.find_element_by_tag_name('button').click()
        time.sleep(1)
        self.driver=driver
        driver.get('http://walle.zhulong.dj:8484/筑龙学社/deploy/index')
    def exit(self):
        driver = self.driver
        driver.quit()
        sys.exit()
handle = WallHandle()
info='''请输入你的选择：
         1.更新git代码并正式服务器
         2.更新git代码并上线预发布服务器
         3.上线到正式服务器
         4.上线到预发布服务器
         5.更新git代码
         6.--更新到online--
         7.打标签
         8.登录
         9.退出
'''
while 1==1 : 
    print(info)
    inputstr=raw_input("请选择:")
    if inputstr =="1":
        handle.handleExec(60)
    elif inputstr=='2':
        handle.handleExec(59)
    elif inputstr=='3':
        handle.publish(60)
    elif inputstr=='4':
        handle.publish(59)
    elif inputstr=='5':
        handle.gitpull()
    elif inputstr=='6':
        handle.gitpullonline()
    elif inputstr=='7':
        handle.tag()
    elif inputstr=='8':
       handle.login()
    elif inputstr=='9':
        handle.exit()
    else:
        pass





