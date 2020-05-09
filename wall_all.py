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
                print(index)
                r.execute(index)
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
        driver = webdriver.Chrome()
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        driver = webdriver.Chrome(chrome_options=options)
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
        #60 线上 59 测试
        driver.get('http://walle.zhulong.dj:8484/筑龙学社/task/create/'+str(num))
        time.sleep(2)
        #driver.find_elements_by_tag_name("input").send_keys('111')
        driver.find_elements_by_class_name("el-input__inner")[0].send_keys(tagname)
        # inputs = driver.find_elements_by_tag_name("input")
        # for i in inputs:
        #     if i.get_attribute("placeholder") == "选取Tag":
        #       i.click()
        #       time.sleep(1)
        #       el=driver.find_elements_by_class_name("el-select-dropdown__item")
        #       text=el[0].find_element_by_tag_name("span").text
        #       driver.find_elements_by_class_name("el-input__inner")[0].send_keys(text)
        #       el[0].find_element_by_tag_name("span").click()
        #       break
        driver.find_elements_by_class_name("el-button")[1].click()
        time.sleep(2)
        driver.get('http://walle.zhulong.dj:8484/筑龙学社/deploy/index')
        time.sleep(2)
        buttons=driver.find_elements_by_class_name("el-button--text")
        for i in buttons:
            print(i.find_element_by_tag_name("span").text)
            if i.find_element_by_tag_name("span").text == "上线":
                i.click()
                break
        time.sleep(2)        
        driver.find_element_by_class_name("el-button--success").click()
        time.sleep(20)
    def handleExec(self,num):
        date = datetime.datetime.today()
        nowtime = date.strftime("%Y%m%d%H%M%S")
        lines='''git fetch --all
        git pull --all
        git fetch origin crmsaller_20191014:crmsaller_20191014
        git merge crmsaller_20191014
        git push
        git push  origin master
        '''
        self.gitExe("D:/htdocs/online-crm",lines)
        info=self.getLogDesc("D:/htdocs/online-crm")
        tagname = '筑龙后台-'+nowtime+'-修改-'+info
        tagnameGBK=tagname.decode('utf-8').encode('GBK')
        lines='git tag '+tagnameGBK
        self.gitExe("D:/htdocs/online-crm",lines)
        lines='git push origin master tag '+tagnameGBK
        self.gitExe("D:/htdocs/online-crm",lines)
        self.viewHandle(tagname,num)

handle = WallHandle()
handle.handleExec(59)



