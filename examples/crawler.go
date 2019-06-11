package main

// NOTE: While the task is good for driving API design, this
// implementation is - by design - sequential, and can't make
// use of the concurrency management offered by scheduler. Instead,
// to better demonstrate the use case, we should have a second job
// which gets the name of the first commenter for every post.

import (
  "log"
  "sync"
  "errors"
  "net/http"
  "github.com/PuerkitoBio/goquery"
 // "github.com/hidden-alphabet/scheduler"
  ".."
)

const RibbonFarmCrawlJob = "RibbonFarmCrawlJob"

type CrawlJob struct {
  URL string
  Titles *[]string
  Mutex *sync.Mutex
}

/*
  Crawls through Ribbon Farm's pagination to get the title of every ribbonfarm post
*/
func main() {
  println("Creating scheduler...")

  s, err := scheduler.New()
  if err != nil {
    log.Fatal(err)
  }

  println("Registering Ribbon Farm Crawler Worker...")

  s.RegisterWorker(RibbonFarmCrawlJob, func(ctx interface{}) *scheduler.WorkerOutput {
    output := &scheduler.WorkerOutput{}

    println("Starting job...")

    job, ok := ctx.(CrawlJob)
    if !ok {
      output.Error = errors.New("Unable to cast context to CrawlJob.")
      return output
    }

    println("Downloading HMTL from: ", job.URL)

    res, err := http.Get(job.URL)
    if err != nil {
      output.Error = err
      return output
    }

    document, err := goquery.NewDocumentFromReader(res.Body)
    if err != nil {
      output.Error = err
      return output
    }

    document.Find("div.post").Each(func(i int, s *goquery.Selection) {
      job.Mutex.Lock()
      *job.Titles = append(*job.Titles, s.Text())
      job.Mutex.Unlock()
    })

    if link, exists := document.Find("div.navigation").Find("li.navigation-next").Find("a").Attr("href"); exists {
      crawlJob := s.NewJob(RibbonFarmCrawlJob, CrawlJob{
        URL: link,
        Titles: job.Titles,
        Mutex: job.Mutex,
      })
      output.Jobs = append(output.Jobs, crawlJob)
    }

    return output
  })

  titles := []string{}

  println("Starting...")

  err = s.AddJob(s.NewJob(RibbonFarmCrawlJob, &CrawlJob{
    URL: "https://ribbonfarm.com",
    Titles: &titles,
    Mutex: &sync.Mutex{},
  }))
  if err != nil {
    log.Fatal(err)
  }

  <-s.Done
}
