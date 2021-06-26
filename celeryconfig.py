
# go celery config
task_serializer = 'json'
accept_content = ['json']  # Ignore other content
result_serializer = 'json'
enable_utc = True
task_protocol=1
# go celery config end

broker_url = 'redis://'
#result_backend = 'rpc://'

#timezone = 'Europe/Oslo'
