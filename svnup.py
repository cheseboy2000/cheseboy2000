# -- coding: utf-8 --
import sys
import paramiko 
reload(sys)
sys.setdefaultencoding('utf8')
class SshHandel:
	def __init__(self):
		ssh = paramiko.SSHClient()
		#创建一个ssh的白名单
		know_host = paramiko.AutoAddPolicy()
		#加载创建的白名单
		ssh.set_missing_host_key_policy(know_host)
		self.ssh=ssh
		self.concent()
	def concent(self):
		self.ssh.connect(
		    hostname = "192.168.1.13",
		    port = 22,
		    username='root'  ,
		    password='zhulong123'
		)
	def change(self,ip):
		stdin, stdout, stderr = self.ssh.exec_command('ssh root@'+ip)
	def exe(self,command):
		stdin, stdout, stderr = self.ssh.exec_command(command)  # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值
		# 打印执行结果
		getStr=stdout.read()
		print(stderr.read())
		return getStr
	def close(self):
		self.ssh.close()

class WindowHandle:
	def __init__(self):
		self.hosts={'edu1':'39.97.236.212','edu2':'39.97.236.229'}
		self.SshHandel=SshHandel()
	def open(self):
		print('''
	    * - - - - - - - - - - - - - - - - - *     
	                   菜单                     
	                1>切换服务器                 
	                2>执行命令
	                3>退出
	    * - - - - - - - - - - - - - - - - - *
''')
		while 1==1:
			showStr='请输入你要执行的操作：\n'
			choice = raw_input(showStr)
			try:
				choice=int(choice)
			except Exception :
				pass
			if choice ==1 :
				print("请选择服务器")
				for key,value in self.hosts.items():
					print(key+"--->"+value)
				ip = raw_input("请输入ip:")
				self.SshHandel.change(ip)
			elif choice ==2 :
				while 1==1:
					command = raw_input("请输入命令(输入exit返回):")
					if command=="exit":
						break
					result=self.SshHandel.exe(command)
					print("执行结果:------------------")
					print(result)
					print("------------------")

			elif choice ==3 :
				sys.exit()
			else:
				pass
window=WindowHandle()
window.open()