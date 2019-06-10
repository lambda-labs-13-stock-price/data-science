package workers

type Job struct {
  Kind string
  Info *interface {}
}

type Processor func(Job) (Job[], error)

type Worker struct {
  Id int
  JobQueue chan Job
  WorkerQueue chan Worker
  Process Processor
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
