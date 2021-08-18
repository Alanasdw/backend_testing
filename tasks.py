from celery import Celery
import subprocess
import time
from datetime import datetime

app = Celery('tasks', broker='redis://localhost', result_backend='redis://localhost')
app.config_from_object('celeryconfig')

@app.task
def add(x, y):
    time.sleep(1)
    return datetime.now()

@app.task
def important(x, y):
    time.sleep(10)
    return datetime.now()

@app.task
def run( CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING):
    return subprocess.call(['./run.sh', CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING])

@app.task
def compare( strict: bool, answer_path: str, target_output_path: str, judge_output_path: str) -> str:
    file = open(judge_output_path, 'r')
    judge = file.read()
    file.close()

    if "success" not in judge:
        # error conditions
        status = "TLE"

        return status
    
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
    
    result = "WA"

    if strict == False:
        answer = strip(answer)
        target = strip(target)
    
    if answer == target:
        result = "AC"
    
    return result


@app.task
def compile( source_name):
    #./run.sh CONTAINER_PATH LANG_ID COMPILED INPUT OUTPUT ERROR TIME_LIMIT MEMORY_LIMIT FILE_LIMIT SECCOMP_STRING
    # call something like gcc and the arguments inside
    return subprocess.call(['gcc', source_name])
    # subprocess.checkoutput() this can get stdout/stderror

@app.task
def execute( source_name):
    #./run.sh CONTAINER_PATH LANG_ID COMPILED INPUT OUTPUT ERROR TIME_LIMIT MEMORY_LIMIT FILE_LIMIT SECCOMP_STRING
    # call something like gcc and the arguments inside
    return subprocess.call(source_name)
    
