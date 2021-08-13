
# # go celery config
# task_serializer = 'json'
# accept_content = ['json']  # Ignore other content
# result_serializer = 'json'
# enable_utc = True
# task_protocol=1
# # go celery config end

broker_url = 'redis://localhost:6379'
result_backend = 'redis://localhost:6379'

broker_transport_options = {'queue_order_strategy': 'priority',}

#timezone = 'Europe/Oslo'
