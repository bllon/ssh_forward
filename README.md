# ssh_forward
ssh端口转发工具2.0

配置端口转发config.json文件
例如
{
  "ssh": {
    "user": "用户名",
    "password": "密码",
    "ssh_host": "跳板机ip",
    "ssh_port": 22,
    "local_host": "127.0.0.1",
    "list": [
      {
        "local_port": 6379,
        "remote_host": "redis服务ip",
        "remote_port": 6379
      }
    ]
  }
}

启动
forward.exe