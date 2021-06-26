from celery import Celery
import subprocess
import time
from datetime import datetime

app = Celery('tasks', broker='redis://localhost', result_backend='redis://localhost')
app.config_from_object('celeryconfig')

@app.task
def add(x, y):
    time.sleep(5)
    return datetime.now()

@app.task
def important(x, y):
    time.sleep(10)
    return datetime.now()

@app.task
def run( CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING):
    return subprocess.call(['./run.sh', CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING])

@app.task
def compile( CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING):
    #./run.sh CONTAINER_PATH LANG_ID COMPILED INPUT OUTPUT ERROR TIME_LIMIT MEMORY_LIMIT FILE_LIMIT SECCOMP_STRING
    # call something like gcc and the arguments inside
    return subprocess.call(['gcc', source_name])
    
