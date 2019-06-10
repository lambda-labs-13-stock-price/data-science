package main

import (
  "os"

  "./workers"
)

func main() {
  workerQueue := workers.New(20)

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
