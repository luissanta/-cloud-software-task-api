broker_url='redis://:G8heLqPFiLWURyiEcmvYwaoICVvLt0xjZAzCaPwPnJ8=@myredis2.redis.cache.windows.net:6379/0'
result_backend='redis://:G8heLqPFiLWURyiEcmvYwaoICVvLt0xjZAzCaPwPnJ8=@myredis2.redis.cache.windows.net:6379/0'
task_serializer='json'
result_serializer='json'
imports=(
    'app.celery.tasks_celery'
)
