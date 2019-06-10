package workers

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

func New() chan Worker {
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

  return workerQueue
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
