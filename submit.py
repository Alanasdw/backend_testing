from celery import Celery
import subprocess

app = Celery('tasks',
    broker='redis://localhost:6379',
    backend='redis://localhost:6379'
)

app.conf.broker_transport_options = {
    'queue_order_strategy': 'priority',
}

@app.task
def add(x, y):
    return x + y

@app.task
def run( CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING):
    return subprocess.call(['./run.sh', CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING])

@app.task
def compile( source_name):
    #./run.sh CONTAINER_PATH LANG_ID COMPILED INPUT OUTPUT ERROR TIME_LIMIT MEMORY_LIMIT FILE_LIMIT SECCOMP_STRING
    # call something like gcc and the arguments inside
    return subprocess.call(['gcc', source_name])

@app.task
def execute( source_name):
    #./run.sh CONTAINER_PATH LANG_ID COMPILED INPUT OUTPUT ERROR TIME_LIMIT MEMORY_LIMIT FILE_LIMIT SECCOMP_STRING
    # call something like gcc and the arguments inside
    return subprocess.call(source_name)

# highest priority 255
# lowest/default priority 0

if __name__ == '__main__':
    #CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING
    for i in range(10):
        ar = add.apply_async((5456, 2878), priority = 90)
    name = "test.c"
    answer = compile.apply_async([name], priority = 10)

    running = execute.apply_async(["./a.out"], priority = 5)


    print( ar.get())
    print( answer.get())
    print( running.get())

