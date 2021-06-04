import pymysql
from git import Repo
from git import Git
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
import sys
import os
import paramiko
class WallHandle:
    def sshInit(self):
        #创建一个ssh的客户端，用来连接服务器
        ssh = paramiko.SSHClient()
        #创建一个ssh的白名单
        know_host = paramiko.AutoAddPolicy()
        #加载创建的白名单
        ssh.set_missing_host_key_policy(know_host)
        
        #连接服务器
        ssh.connect(
            hostname = "192.168.1.13",
            port = 22,
            username = "root",
            password = "zhulong123"
        )
        
        #执行命令
        stdin,stdout,stderr = ssh.exec_command("rm -rf /tmp/walle/codebase/*")
        #stdin  标准格式的输入，是一个写权限的文件对象
        #stdout 标准格式的输出，是一个读权限的文件对象
        #stderr 标准格式的错误，是一个写权限的文件对象
        
        print(stdout.read().decode())
        time.sleep(5)
    def dbInit(self):
        # 连接database
        conn = pymysql.connect(host="192.168.1.222", user="zhulong",password="zhulong123456",database="walle",charset="utf8")
        # 得到一个可以执行SQL语句的光标对象
        cur = conn.cursor(pymysql.cursors.DictCursor)
        # 定义要执行的SQL语句
        sql = "select id,name from projects where environment_id=2 and repo_mode='branch' and status=1 and id>=164"
        self.dist={}  
        try:  
            cur.execute(sql)    #执行sql语句  
            results = cur.fetchall()    #获取查询的所有记录  
            #遍历结果  
            for row in results :  
                self.dist[row['name']]=row['id']
        except Exception as e:  
            raise e
        finally :
            pass
        list=['testnewcommon','openbbs','openpay','openedu','openshouye','openvip','openucenter','opencrm','testnewauth','testnewadmin','openpassport']
        list=['opencrm']
        for v in list:
            try: 
                id=self.dist[v]
                sql="select commit_id from tasks where project_id ="+str(id)+" order by id desc limit 1"
                cur.execute(sql)    #执行sql语句  
                results = cur.fetchone()    #获取查询的所有记录  
                commit_id=results['commit_id']
                print(v+":"+str(commit_id))
                self.upProject(id,commit_id)
            except Exception as e:  
                raise e  
            finally :
                pass
        conn.close()  #关闭连接 
    def __init__(self):
        self.sshInit()
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(options=options)
        self.driver=driver
        self.login()
        self.dbInit()
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
    def upProject(self,id,code):
        driver=self.driver
        print('http://walle.zhulong.dj:8484/筑龙学社/task/create/'+str(id))
        driver.get('http://walle.zhulong.dj:8484/筑龙学社/task/create/'+str(id))
        Wait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "wl-task-edit__refresh")))
        try :
            driver.find_elements_by_class_name("wl-task-edit__refresh")[0].click()
        except Exception :
            time.sleep(3)
            driver.find_elements_by_class_name("wl-task-edit__refresh")[0].click()
        if driver.find_elements_by_class_name("el-input__inner")[1].get_attribute("value")!="develop":
            try :
                time.sleep(3)
                driver.find_elements_by_class_name("el-input__inner")[1].click()
            except Exception :
                print("分支点击失败1")
                time.sleep(10)
                try :
                    driver.find_elements_by_class_name("el-input__inner")[1].click()
                except Exception :
                    print("分支点击失败2")
                    return False
            boolean=True
            for el in driver.find_elements_by_class_name("el-select-dropdown__wrap")[1].find_elements_by_class_name("el-select-dropdown__item"):
                if el.find_element_by_tag_name("span").text=="develop":
                    print(el.find_element_by_tag_name("span").text)
                    print("develop click")
                    el.click()
                    try :
                        driver.find_elements_by_class_name("wl-task-edit__refresh")[1].click()
                    except Exception :
                        time.sleep(3)
                        try :
                            driver.find_elements_by_class_name("wl-task-edit__refresh")[1].click()
                        except Exception :
                            print("刷新版本号失败")
                            return False
                    time.sleep(3)
                    boolean=False
            if boolean :
                try :
                    driver.find_elements_by_class_name("el-select-dropdown__wrap")[1].find_elements_by_class_name("el-select-dropdown__item")[0].click()
                except Exception :
                    print("下拉点击失败")
                    return False
        time.sleep(5)
        try :
            driver.find_elements_by_class_name("el-input__inner")[2].click()
        except Exception :
            time.sleep(3)
            try :
                driver.find_elements_by_class_name("el-input__inner")[2].click()
            except Exception :
                print("下拉点击失败2")
                return False
        try :
            driver.find_elements_by_class_name("el-select-dropdown__wrap")[1].find_elements_by_class_name("el-select-dropdown__item")[0].click()
        except Exception :
            time.sleep(3)
            try :
                driver.find_elements_by_class_name("el-select-dropdown__wrap")[1].find_elements_by_class_name("el-select-dropdown__item")[0].click()
            except Exception :
                print("下拉点击失败3")
                return False
        text=driver.find_elements_by_class_name("el-input__inner")[2].get_attribute("value")
        if text.find(code)>-1 :
            print("版本一致:"+code)
            return
        date = datetime.datetime.today()
        nowtime = date.strftime("%Y%m%d%H%M%S")
        print("上线"+text)
        driver.find_elements_by_class_name("el-input__inner")[0].send_keys(str(nowtime))
        try :
            driver.find_elements_by_class_name("el-button")[1].click()
            time.sleep(2)
        except Exception :
            try :
                time.sleep(3)
                driver.find_elements_by_class_name("el-button")[1].click()
                time.sleep(2)
            except Exception :
                print("异常")
                return 
        driver.get('http://walle.zhulong.dj:8484/筑龙学社/deploy/index')
        time.sleep(2)
        buttons=driver.find_elements_by_class_name("el-button--text")
        for i in buttons:
            if i.find_element_by_tag_name("span").text == "上线":
                try :
                    i.click()
                except Exception :
                    print("异常")
                    return 
                break
        time.sleep(2)
        try :    
            driver.find_element_by_class_name("el-button--success").click()
        except Exception :
            time.sleep(5)
            driver.find_element_by_class_name("el-button--success").click()
        time.sleep(20)
        driver.get('http://walle.zhulong.dj:8484/筑龙学社/deploy/index')

handle = WallHandle()
handle.driver.quit()