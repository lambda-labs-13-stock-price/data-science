package main

import (
  "os"

  "./workers"
)

func main() {
	workerCount := 20
	workerQueue := make(chan *workers.Worker, workerCount)

  /*
    Instantiating worker goroutines to do work as they
    become ready.
  */
	for i := 0; i < workerCount; i++ {
		worker := &workers.Worker{
			Id: i,
			JobQueue: make(chan workers.Job),
			WorkerQueue: workerQueue,
		}

		go worker.Work()

		workerQueue <- worker
	}

  /*
    When a task is available for a worker to do, we parse it
    into a standard format to determine what kind of worker
    should undertake the given task.

    Having made that decision we construct the appropriate
    context for that worker, wait for a worker to become
    available from the worker queue, and wait again for
    tasks to become available.
  */
  for todo := range Todos {
    job := &worker.Job{
      Kind: "Crawl"
      Info: &CrawlingJob{
      }
    }

    worker := <-workerQueue
    worker.JobQueue <- job
  }
}
