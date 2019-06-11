package scheduler

import (
  "time"
)

/*
  A WorkerOutput is the required output of a worker function 
*/
type WorkerOutput struct {
  Jobs []*Job
  Error error
}

/*
  A Worker is a function which carries out some task using 
  a Job object as context, and returning a WorkerOutput object. 
*/
type Worker func(interface{}) *WorkerOutput

/*
  A Job is an arbitrary object for providing context to each 
  worker during execution.
*/
type Job struct {
  Name string
  Context interface{}
}

/*
  A Task is an object for managings goroutines. It provides each 
  goroutine with a jobs queue to execute upon and access to its
  supervising Scheduler object.
*/
type Task struct {
  Jobs        chan *Job
	Scheduler   *Scheduler
}

/*
  Scheduler's manage a queue of goroutines, distributing work
  to them when they become available. It keeps a count of the
  number of total and active tasks at any given moment.
*/
type Scheduler struct {
  TotalTasks int
  ActiveTasks int

  Tasks chan *Task
  Registrar map[string]Worker

  Done chan bool
}

/*
  Create a new scheduler. 
*/
func New() (*Scheduler, error) {
  scheduler := &Scheduler{
    TotalTasks: 0,
    Registrar: make(map[string]Worker),
  }

  err := scheduler.Scale(1)
  if err != nil {
    return nil, err
  }

	return scheduler, nil
}

/*
  Increase the number of tasks available to do work by n. 
*/
func (s *Scheduler) Scale(n int) error {
  current := s.TotalTasks

  for id := current; id < current+n; id++ {
    task := &Task{
      Scheduler:      s,
    }

    go task.Run()

    println("Adding task to queue")

    go func() {
      s.Tasks <- task
      s.TotalTasks += 1
    }()
  }

  return nil
}

/*
  Create a new worker.
*/
func (s *Scheduler) RegisterWorker(name string, worker Worker) {
  s.Registrar[name] = worker
}

/*
  Create a new job.
*/
func (s *Scheduler) NewJob(name string, ctx interface{}) *Job {
  return &Job{
    Name: name,
    Context: ctx,
  }
}

/*
  Schedule a job to be done.
*/
func (s *Scheduler) AddJob(job *Job) error {
  select {
    case t := <-s.Tasks:
      s.ActiveTasks += 1
      t.Jobs <- job
    case <-time.After(1 * time.Second):
      err := s.Scale(1)
      if err != nil {
        return err
      }

      err = s.AddJob(job)
      if err != nil {
        return err
      }
  }

  return nil
}

/*
  Start a worker to listen for available work to be done from
  a job queue.
*/
func (t *Task) Run() {
  registrar := t.Scheduler.Registrar

	for job := range t.Jobs {
    worker := registrar[job.Name]
    context := job.Context

    output := worker(context)
    if output != nil && len(output.Jobs) != 0 {
      for _, job := range output.Jobs {
        t.Jobs <- job
      }
    }

    t.Scheduler.Tasks <- t
    t.Scheduler.ActiveTasks -= 1
	}
}
