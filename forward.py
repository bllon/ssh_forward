from sshtunnel import SSHTunnelForwarder
import threading
import socket
import os
import sys

# 获取项目根目录
def app_path():
    if hasattr(sys, 'frozen'):
        return os.path.dirname(os.path.dirname(os.path.dirname(sys.executable))) #使用pyinstaller打包后的exe目录
    return os.path.dirname(__file__)

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

app_path = app_path()

#局域网ip
local_host = get_host_ip()

def forwardSSH(user,password,ssh_host,ssh_port,local_host,local_port,remote_host,remote_port):
    server = SSHTunnelForwarder(
            ssh_username=user,
            ssh_password=password,
            ssh_address_or_host=(ssh_host, ssh_port),
            local_bind_address=(local_host, local_port),
            remote_bind_address=(remote_host, remote_port)
    )
    # 守护线程
    server.daemon_forward_servers=False
    server.start()
    if server.is_active:
        print('本地端口{}:{}已转发至远程端口{}:{}'.format(local_host,server.local_bind_port,remote_host,remote_port))
    else :
        print('本地端口{}:{}转发失败,请重试')

#读取配置文件
with open(app_path + '/config.txt') as f:
    lines = f.readlines()
    t = locals()
    i = 1
    for line in lines:
        data = line.split(",")

        user = str(data[0].strip("\'"))
        password = str(data[1].strip("\'"))
        ssh_host = str(data[2].strip("\'"))
        ssh_port = int(data[3].strip("\'"))
        local_port = int(data[4].strip("\'"))
        remote_host = str(data[5].strip("\'"))
        remote_port = int(data[6].rstrip("\n").strip("\'"))
        #print(local_port,remote_host,remote_port)
        t[str(i)] = threading.Thread(forwardSSH(user,password,ssh_host,ssh_port,local_host,local_port,remote_host,remote_port))
        t[str(i)].start()

