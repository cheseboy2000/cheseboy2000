# -- coding: utf-8 --
import time
import datetime
from selenium import webdriver
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
driver.get('https://passport.zhulong.com/user/login?redirecturl=https://passport.zhulong.com/user/staff?pingce_time='+lastmonth)
driver.execute_script("return $('#btns li:eq(1)')[0]").click()
driver.find_element_by_id('Uname').send_keys(u'黄小梨')
driver.find_element_by_id('password').send_keys('tenenl111')
driver.find_elements_by_class_name('denglu_btn')[0].click()
ep=driver.find_elements_by_name("ep")
eve_name=driver.find_elements_by_name("eve-name")
btn_next=driver.find_elements_by_class_name("btn-next")
for i in range(4):
	for k in range(5):
		for t in eve_name:
			if t.is_displayed() and (not t.is_selected()):
				t.click()
				for e in ep:
					if e.is_displayed():
						t.click()
						break
		for b in btn_next:
			if b.is_displayed():
				b.click()
				break


	#driver.find_elements_by_class_name('btn-next')[0].click()
	# driver.find_elements_by_class_name('btn-next')[0].click()
	

