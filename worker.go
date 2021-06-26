// package worker

import (
	"time"

	"github.com/gocelery/gocelery"
	"github.com/gomodule/redigo/redis"
)

func worker() {
	// create redis connection pool
	redisPool := &redis.Pool{
		Dial: func() (redis.Conn, error) {
			c, err := redis.DialURL("redis://")
			if err != nil {
				return nil, err
			}
			return c, err
		},
	}

	// initialize celery client
	cli, _ := gocelery.NewCeleryClient(
		gocelery.NewRedisBroker(redisPool),
		&gocelery.RedisCeleryBackend{Pool: redisPool},
		5, // number of workers
	)

	// task
	// the task the worker needs to perform
	// could be more than one in here ??
	add := func(a, b int) int {
		return a + b
	}

	// register task
	// the task looks like it only needs one register??
	cli.Register("worker.add", add)

	// start workers (non-blocking call)
	cli.StartWorker()

	// wait for client request
	time.Sleep(10 * time.Second)

	// stop workers gracefully (blocking call)
	cli.StopWorker()

}
