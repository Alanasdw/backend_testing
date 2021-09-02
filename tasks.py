from celery import Celery
import subprocess
import time
from datetime import datetime

app = Celery('tasks', broker='redis://localhost:6379', result_backend='redis://localhost:6379')
# app.config_from_object('celeryconfig')
app.conf.broker_transport_options = {
    'queue_order_strategy': 'priority',
}
# app.conf.task_send_succeeded_task = True

@app.task
def add(x, y):
    time.sleep(1)
    return datetime.now()

@app.task
def important(x, y):
    time.sleep(10)
    return datetime.now()

@app.task
def compile( source_name):
    #./run.sh CONTAINER_PATH LANG_ID COMPILED INPUT OUTPUT ERROR TIME_LIMIT MEMORY_LIMIT FILE_LIMIT SECCOMP_STRING
    # call something like gcc and the arguments inside
    return subprocess.call(['gcc', source_name])
    # subprocess.checkoutput() this can get stdout/stderror

@app.task
def execute( source_name: str):
    #./run.sh CONTAINER_PATH LANG_ID COMPILED INPUT OUTPUT ERROR TIME_LIMIT MEMORY_LIMIT FILE_LIMIT SECCOMP_STRING
    # call something like gcc and the arguments inside
    return subprocess.call(source_name)


@app.task
def run( CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING):
    return subprocess.call(['/home/linux/Desktop/nsjail/run.sh', CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING, '/home/linux/Desktop/nsjail/'])

@app.task
def compare( strict: bool, answer_path: str, target_output_path: str, judge_output_path: str) -> str:
    # ['SUCCESS','RE','TLE','OLE','MLE','JGE','CE','NO SRC']
    file = open(judge_output_path, 'r')
    judge_out = file.read()
    file.close()

    result = [ item for item in judge_out.splitlines()]

    if "SUCCESS" != result[ 0]:
        # error conditions
        return result[ 0]
    
    file = open(answer_path,'r')
    answer = file.read()
    file.close()

    file = open(target_output_path,'r')
    target = file.read()
    file.close()

    def strip(s: str):
        # remove blanks at line end
        striped = [ s.rstrip() for s in s.splitlines()]
        # remove blanks at file end
        while len( striped) and striped[-1] == '':
            striped.pop(-1)
        return striped
    
    result[ 0] = "WA"

    if strict == False:
        answer = strip(answer)
        target = strip(target)
    
    if answer == target:
        result[ 0] = "AC"
    
    return result[ 0]

