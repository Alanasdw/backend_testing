from threading import main_thread
from celery import Celery
import celery
from celery.result import AsyncResult
import time
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
def important(x, y):
    time.sleep(10)
    return datetime.now()

@app.task
def compile( source_name):
    #./run.sh CONTAINER_PATH LANG_ID COMPILED INPUT OUTPUT ERROR TIME_LIMIT MEMORY_LIMIT FILE_LIMIT SECCOMP_STRING
    # call something like gcc and the arguments inside
    return subprocess.call(['gcc', source_name])

@app.task
def execute( source_name: str):
    #./run.sh CONTAINER_PATH LANG_ID COMPILED INPUT OUTPUT ERROR TIME_LIMIT MEMORY_LIMIT FILE_LIMIT SECCOMP_STRING
    # call something like gcc and the arguments inside
    return subprocess.call(source_name)

@app.task
def run( CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING):
    return subprocess.call(['./run.sh', CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING])

@app.task
def compare( strict: bool, answer_path: str, target_output_path: str, judge_output_path: str) -> str:
    file = open(judge_output_path, 'r')
    judge_out = file.read()
    file.close()

    result = [ item for item in judge_out.splitlines()]

    if "SUCCESS" not in result[ 0]:
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

# largest priority 255
# smallest/default priority 0
# redis priority is ( high, 0) -> ( low, 9)

if __name__ == '__main__':
    # CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING
    # /home/linux/Desktop/backend_testing/ 0 0 /home/linux/Desktop/backend_testing/README.md /home/linux/Desktop/backend_testing/README.md /home/linux/Desktop/backend_testing/judge.txt 1 512 512 "read, newfstat, mmap, mprotect, munmap, newuname, arch_prctl, brk, access, exit_group, close, readlink, sysinfo, write, writev, lseek, clock_gettime, fcntl, pread64, openat, newstat"
    # CONTAINER_PATH = "/home/linux/Desktop/backend_testing/"
    # LANG_ID = "0"
    # COMPILED = "0"
    # INPUT = "/home/linux/Desktop/backend_testing/input.txt"
    # OUTPUT = "/home/linux/Desktop/backend_testing/output.txt"
    # ERROR = "/home/linux/Desktop/backend_testing/judge.txt"
    # TIME_LIMIT = "10"
    # MEMORY_LIMIT = "512"
    # FILE_LIMIT = "512"
    # SECCOMP_STRING = "read, newfstat, mmap, mprotect, munmap, newuname, arch_prctl, brk, access, exit_group, close, readlink, sysinfo, write, writev, lseek, clock_gettime, fcntl, pread64, openat, newstat"

    # testing = run.apply_async([CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING], priority = 9)
    # print(testing.get())
    s = "./main"
    executing = celery.signature( 'tasks.execute', args=[s], immutable=True, priority=4)
    c = celery.chain( executing, compare.signature([False,"/home/linux/Desktop/backend_testing/answer.txt","/home/linux/Desktop/backend_testing/output.txt","/home/linux/Desktop/backend_testing/judge.txt"], immutable=True, priority=0))
    g = celery.group( [important.s(y,y).set(priority=9) for y in range(4)] + [add.s(x,x).set(priority=7) for x in range(10)])
    res2 = g()
    res = c()

    print(res.get())
    print(res2.get())


    # for i in range(10):
    # ar = add.apply_async((5456, 2878), priority = 9)
    # name = "test.c"
    # answer = compile.apply_async([name], priority = 5)
    # ar = add.apply_async((5456, 2878), priority = 9)
    # running = execute.apply_async(["./a.out"], priority = 0)

    # print( AsyncResult( ar.task_id).ready())

    # print( ar.get())
    # print( answer.get())
    # print( running.get())

    # print( AsyncResult( ar.task_id).ready())

    # # how the code could look like
    # # all the code should look like main.*
    # CONTAINER_PATH = "/somewhere"
    # LANG_ID = 0
    # COMPILED = 0
    # if LANG_ID == 2:
    #     # its python code
    #     COMPILED = 1
    
    # # ideally this should have a bug bunch of individual files
    # INPUT = [ "/somewhere/input_num"] 
    # OUTPUT = [ "/somewhere/output_num"] 
    # ERROR = [ "/somewhere/result_num"]

    # TIME_LIMIT = 1
    # MEMORY_LIMIT = 512
    # FILE_LIMIT = 512
    # SECCOMP_STRING = "\"read, newfstat, mmap, mprotect, munmap, newuname, arch_prctl, brk, access, exit_group, close, readlink, sysinfo, write, writev, lseek, clock_gettime, fcntl, pread64, openat, newstat\""
    # task_ids = []
    # # first compile the code
    # # compile will need to be at a low priority
    # if LANG_ID == 0 or LANG_ID == 1:
    #     compileing = run.apply_async([ CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING], priority = 90)
    #     task_ids.append( compileing.task_id)
    #     # if failed just write CE to all files
    #     # get() will lead to 0 normally
    #     # read error file to know the result
    #     # this while is to wait ( blocking?)
    #     while 1:
    #         if AsyncResult( task_ids[ 0]) == True:
    #             # do stuff
    #             # if CE or something
    #             # return 1
    #         else:
    #             # sleep for some time
    #             time.sleep( 1)
    
    # # update the arguments
    # COMPILED = 1

    # # then add all the tasks to the broker
    # for i in range( len( INPUT) - 1):
    #     cases = run.apply_async([ CONTAINER_PATH, LANG_ID, COMPILED, INPUT[ i + 1], OUTPUT[ i + 1], ERROR[ i + 1], TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING], priority = 5)
    #     task_ids.append( cases.task_id)

    # # wait for the results
    # # check all the task ids
    # while 1:
    #     finished = 1
    #     for i in range( len( INPUT)):
    #         if AsyncResult( task_ids[ i]) == False:
    #             finished = 0
    #             break
    #     if finished == 1:
    #         # finished
    #         # do stuff
    #     else:
    #         # not finished
    #         # sleep for some time
    #         time.sleep( 1)
    
    # return 0
