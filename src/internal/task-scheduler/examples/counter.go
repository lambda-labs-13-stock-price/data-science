package main

import (
  "github.com/hidden-alphabet/scheduler"
)

type CounterJob {
  Count *int
}

/*
  A 
*/
func main() {
  conut := 0

  s := scheduler.New()

  s.NewWorker("CounterJob", func(j *Job) *WorkerOutput {
    if count, ok := j.Properties.(CounterJob) {
      count += 1
    }
  })

  s.Jobs <- s.NewJob("CounterJob", CounterJob{ Count: &count })

  <-s.Done
}
