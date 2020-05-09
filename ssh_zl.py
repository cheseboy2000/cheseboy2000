# -- coding: utf-8 --
import sys
import paramiko 
# 上传文件
def sftp_upload_file(server_path, local_path):
    try:
        t = paramiko.Transport((ip, 22))
        t.connect(username=user, password=pwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, server_path)
        t.close()
    except Exception as  e:
        print(e)

# 下载文件
def sftp_down_file(server_path, local_path):
    try:
        t = paramiko.Transport((ip, 22))
        t.connect(username=user, password=pwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path)
        t.close()
    except Exception as e:
        print(e)

# 连接
def ssh_conn(ip, cmd):

    ssh = paramiko.SSHClient()
    # 允许连接不在known_hosts文件上的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(ip, 22, user, pwd)
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(cmd)
    # 获取结果
    print(10 * "-", 'start', 10 * "-")
    for line in stdout:
        res=(line.strip('\n').split())
        print(res)
    else:
        print(stdout)
    print(10 * "-", 'end', 10 * "-")

def menu():
    print('''
    * - - - - - - - - - - - - - - - - - *     
                   菜单                     
                1>上传文件                 
                2>下载文件
                3>执行命令
                4>退出
    * - - - - - - - - - - - - - - - - - *
    ''')

    choice = int(input('请输入你要执行的操作：\n'))
    if choice == 1:
        src = input('请输入原路径：\n')
        dest = input('请输入目标路径：\n')
        sftp_upload_file(src, dest)
    elif choice == 2:
        src = input('请输入原路径：\n')
        dest = input('请输入目标路径：\n')
        sftp_down_file(src, dest)
    elif choice == 3:
        while True:
            cmd = input('请输入要执行的命令：\n')
            if cmd == 'eixt':
                sys.exit()
            ssh_conn(ip, cmd)
    else:
        sys.exit()

#创建一个ssh的客户端，用来连接服务器
ssh = paramiko.SSHClient()
#创建一个ssh的白名单
know_host = paramiko.AutoAddPolicy()
#加载创建的白名单
ssh.set_missing_host_key_policy(know_host)
ssh.connect(hostname='39.97.235.87', port=2222, username='tanlei', password='amtb791127')
# # 打开一个Channel并执行命令
# stdin, stdout, stderr = ssh.exec_command('df -h ')  # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值
 
# # 打印执行结果
# getStr=stdout.read().decode('utf-8')
# print(getStr);
# 关闭SSHClient
ssh.close()