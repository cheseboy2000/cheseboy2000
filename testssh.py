# -- coding: utf-8 --
import sys
import paramiko 
arg0=sys.argv[0]
#创建一个ssh的客户端，用来连接服务器
ssh = paramiko.SSHClient()
#创建一个ssh的白名单
know_host = paramiko.AutoAddPolicy()
#加载创建的白名单
ssh.set_missing_host_key_policy(know_host)
# 实例化一个私钥对象 /root/.ssh
private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
#连接服务器
ssh.connect(
    hostname = "39.97.231.102",
    port = 22,
    pkey= private_key ,
)
# 打开一个Channel并执行命令
stdin, stdout, stderr = ssh.exec_command('df -h ')  # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值
 
# 打印执行结果
getStr=stdout.read().decode('utf-8')
print(getStr);
# 关闭SSHClient
ssh.close()