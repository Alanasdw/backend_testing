package main

import (
	"fmt"
	"log"
	"math/rand"
	"reflect"
	"time"

	"github.com/gocelery/gocelery"
	"github.com/gomodule/redigo/redis"
)

func main() {
	fmt.Println("Hello, World!")

	// create redis connection pool
	redisPool := &redis.Pool{
		Dial: func() (redis.Conn, error) {
			c, err := redis.DialURL("redis://localhost")
			// fmt.Println("Hello, World!inside")
			if err != nil {
				return nil, err
			}
			return c, err
		},
	}

	fmt.Println("Hello, World! connected")

	// initialize celery client
	cli, _ := gocelery.NewCeleryClient(
		gocelery.NewRedisBroker(redisPool),
		&gocelery.RedisCeleryBackend{Pool: redisPool},
		1,
	)

	// prepare arguments
	taskName := "tasks.add" //"tasks.compile"
	argA := rand.Intn(10)   //"test.c"
	argB := rand.Intn(10)
	// ( CONTAINER_PATH, LANG_ID, COMPILED, INPUT, OUTPUT, ERROR, TIME_LIMIT, MEMORY_LIMIT, FILE_LIMIT, SECCOMP_STRING)
	// CONTAINER_PATH := "/home/sandbox/Desktop/NOJ/HW4"

	// need to get the language
	// LANG_ID := 0

	// need to create files for input, output, error

	// get limits
	// TIME_LIMIT := 1
	// MEMORY_LIMIT := 1
	// FILE_LIMIT := 1
	// SECCOMP_STRING := "\"read, newfstat, mmap, mprotect, munmap, newuname, arch_prctl, brk, access, exit_group, close, readlink, sysinfo, write, writev, lseek, clock_gettime, fcntl, pread64, openat, newstat\""

	// run task
	// compileResult, err := cli.Delay("tasks.run", CONTAINER_PATH, LANG_ID)
	// if err != nil {
	// 	panic(err)
	// }
	// read from

	// run task
	asyncResult, err := cli.Delay(taskName, argA, argB)
	importantResult, err := cli.Delay("tasks.important", argA, argB)
	if err != nil {
		panic(err)
	}

	fmt.Println("Hello, World! timing out")

	// get results from backend with timeout
	res, err := asyncResult.Get(10 * time.Second)
	resimportant, err := importantResult.Get(10 * time.Second)
	if err != nil {
		panic(err)
	}

	log.Printf("result: %+v of type %+v", resimportant, reflect.TypeOf(resimportant))
	log.Printf("result: %+v of type %+v", res, reflect.TypeOf(res))
}
