# -- coding: utf-8 --
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
lastmonth = getTheMonth(date, 1).strftime("%Y-%m")
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
driver.get('http://walle.zhulong.dj:8484/%E7%AD%91%E9%BE%99%E5%AD%A6%E7%A4%BE/task/create/59')
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




