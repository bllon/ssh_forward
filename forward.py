from sshtunnel import SSHTunnelForwarder
import threading
import socket
import os
import sys
import json


# 获取项目根目录
def app_path():
    if hasattr(sys, 'frozen'):
        return os.path.dirname(sys.executable)  # 使用pyinstaller打包后的exe目录
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

# 局域网ip
local_host = get_host_ip()


def forwardSSH(user, password, ssh_host, ssh_port, local_host, local_port, remote_host, remote_port):
    server = SSHTunnelForwarder(
        ssh_username=user,
        ssh_password=password,
        ssh_address_or_host=(ssh_host, ssh_port),
        local_bind_address=(local_host, local_port),
        remote_bind_address=(remote_host, remote_port)
    )
    # 守护线程
    server.daemon_forward_servers = False
    server.start()
    if server.is_active:
        print('本地端口{}:{}已转发至远程端口{}:{}'.format(local_host, server.local_bind_port, remote_host, remote_port))
    else:
        print('本地端口{}:{}转发失败,请重试')


# 读取json配置文件
try:
    with open(app_path + '/config.json', 'r') as f:
        load_dict = json.load(f)
        ssh_config = load_dict['ssh']
        user = ssh_config['user']
        password = ssh_config['password']
        ssh_host = ssh_config['ssh_host']
        ssh_port = ssh_config['ssh_port']
        if 'local_host' in ssh_config:
            local_host = ssh_config['local_host']
        t = locals()
        i = 1
        for item in ssh_config['list']:
            if 'user' in ssh_config:
                user = ssh_config['user']
            if 'password' in ssh_config:
                password = ssh_config['password']
            if 'ssh_host' in ssh_config:
                ssh_host = ssh_config['ssh_host']
            if 'ssh_port' in ssh_config:
                ssh_port = ssh_config['ssh_port']
            local_port = item['local_port']
            remote_host = item['remote_host']
            remote_port = item['remote_port']
            t[str(i)] = threading.Thread(
                forwardSSH(user, password, ssh_host, ssh_port, local_host, local_port, remote_host, remote_port))
            t[str(i)].start()
except IndexError as e:
    print('配置文件不合法: ', e)