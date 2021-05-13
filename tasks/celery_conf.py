timezone = 'Asia/Shanghai'
accept_content = ['pickle', 'json']
worker_redirect_stdouts_level = 'INFO'

broker_url = 'redis://127.0.0.1:6379/0'
broker_pool_limit = 100
task_serializer = 'pickle'

result_backend = 'redis://127.0.0.1:6379/0'
result_serializer = 'pickle'
result_expires = 3600
result_cache_max = 10000

