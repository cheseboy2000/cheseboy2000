# -- coding: utf-8 --
from git import Repo
from git import Git
import time
import datetime
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def getTheMonth(date, n):
    month = date.month
    year = date.year
    for i in range(n):
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
    return datetime.date(year, month, 1)
date = datetime.datetime.today()
nowtime = date.strftime("%Y%m%d%H%M%S")
print("D:/htdocs/online-crm")
r = Git("D:/htdocs/online-crm")
print("git fetch --all")
r.execute('git fetch --all')
print("git pull --all")
r.execute('git pull --all')
print("git fetch origin crmsaller_20191014:crmsaller_20191014")
r.execute("git fetch origin crmsaller_20191014:crmsaller_20191014")
print("git merge crmsaller_20191014")
r.execute('git merge crmsaller_20191014')
print("git push")
r.execute('git push')
print("git push  origin master")
r.execute('git push  origin master')
status=r.execute('git log -10')
strs=status.split("\n")
info =''
for index in range(6,60,6):
    info=strs[index].replace(' ','')
    if info!='' and info.find("Merge") == -1 :
        break 
tagname = '筑龙后台-'+nowtime+'-修改-'+info
tagnameGBK=tagname.decode('utf-8').encode('GBK')
print('git tag '+tagnameGBK)
r.execute('git tag '+tagnameGBK)
print('git push origin master tag '+tagnameGBK)
r.execute('git push origin master tag '+tagnameGBK)
driver = webdriver.Chrome()
driver.get('http://walle.zhulong.dj:8484/login')
time.sleep(1);
inputs = driver.find_elements_by_tag_name("input")
for i in inputs:
    if i.get_attribute("type") == "text":
        i.send_keys('tanlei@zhulong.com')
    elif i.get_attribute("placeholder") == "请输入密码":
    	i.send_keys('Zhulong123')
driver.find_element_by_tag_name('button').click()
time.sleep(1);
#60 线上 59 测试
driver.get('http://walle.zhulong.dj:8484/%E7%AD%91%E9%BE%99%E5%AD%A6%E7%A4%BE/task/create/60')
time.sleep(2);
#driver.find_elements_by_tag_name("input").send_keys('111')
inputs = driver.find_elements_by_tag_name("input")
for i in inputs:
    if i.get_attribute("placeholder") == "选取Tag":
    	i.click();
    	time.sleep(1);
    	el=driver.find_elements_by_class_name("el-select-dropdown__item");
    	text=el[0].find_element_by_tag_name("span").text
    	driver.find_elements_by_class_name("el-input__inner")[0].send_keys(text)
    	el[0].find_element_by_tag_name("span").click()
    	break
driver.find_elements_by_class_name("el-button")[1].click()
time.sleep(2);
driver.get('http://walle.zhulong.dj:8484/%E7%AD%91%E9%BE%99%E5%AD%A6%E7%A4%BE/deploy/index')
time.sleep(2);
buttons=driver.find_elements_by_class_name("el-button--text")
for i in buttons:
	print(i.find_element_by_tag_name("span").text)
	if i.find_element_by_tag_name("span").text == "上线":
		i.click()
		break
time.sleep(2);
driver.find_element_by_class_name("el-button--success").click()




