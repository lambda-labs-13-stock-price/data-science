package main

import (
  "os"

  "./workers"

  "github.com/aws/aws-sdk-go/aws"
  "github.com/aws/aws-sdk-go/aws/session"
  "github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/sqs"
)

func main() {
	workerCount := 20
	workerQueue := make(chan *workers.Worker, workerCount)

	for i := 0; i < workerCount; i++ {
		worker := &workers.Worker{
			Id: i,
			JobQueue: make(chan workers.Job),
			WorkerQueue: workerQueue,
		}

		go worker.Work()

		workerQueue <- worker
	}

  for todo := range Todos {
    worker := <-workerQueue

    job := &worker.Job{
      Kind: "Crawl"
      Info: &CrawlingJob{
      }
    }

    worker.JobQueue <- job
  }
}
