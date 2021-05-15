# -*- coding: utf-8 -*-

from multiprocessing import cpu_count

bind = ["127.0.0.1:9000"]
daemon = True
pidfile = 'logs/gunicorn.pid'

workers = cpu_count() * 2  # 工作进程数量
# worker_class = "gevent"
worker_class = "egg:meinheld#gunicorn_worker"  # 比 gevent 更快的一个异步网络库
worker_connections = 65535  # 单个进程的最大连接数

keepalive = 60
timeout = 30
graceful_timeout = 10
forwarded_allow_ips = '*'

# 日志处理
capture_output = True
loglevel = 'info'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置

access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'  # 设置gunicorn访问日志格式，错误日志无法设置
accesslog = "logs/access.log"
errorlog = 'logs/error.log'
"""
其每个选项的含义如下：
h          remote address
l          '-'
u          currently '-', may be user name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          user agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
"""
