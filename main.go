package main

import (
  "os"
  "fmt"
  "sql"
  "errors"
	"strings"
  "net/http"
  "github.com/aws/aws-sdk-go/aws"
  "github.com/aws/aws-sdk-go/aws/session"
  "github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/sqs"
)

type Job struct {
  Kind string
  Info *interface {}
}

type Worker struct {
  Id int
  JobQueue chan Job
  WorkerQueue chan Worker
  Process func(Job) (Job[], error)
}

func (w *Worker) Work() {
	for job := range w.JobQueue {
		todos, err := w.Process(job)
    if err != nil {
      log.Print(err)
    }

		for _, todo := range todos {
			w.JobQueue <- todo
		}

		w.WorkerQueue <- w
	}
}

func main() {
	workerCount := 20
	workerQueue := make(chan *Worker, workerCount)

	for i := 0; i < workerCount; i++ {
		worker := &Worker{
			Id: i,
			JobQueue: make(chan Job),
			WorkerQueue: workerQueue,
		}

		go worker.Work()

		workerQueue <- worker
	}

  for todo := range Todos {
    worker := <-workerQueue

    job := &Job{
      Kind: "Crawl"
      Info: &CrawlingJob{
      }
    }

    worker.JobQueue <- job
  }
}
