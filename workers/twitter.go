package workers

import (
  "os"
  "errors"
  "net/url"
  "strings"
  "net/http"

  "github.com/PuerkitoBio/goquery"
)

/*
  Metadata to inform the crawling of twitter.com/search
*/
type CrawlingJob struct {
  Search *string
  TweetCount int
  LastTwitterId string
}

/*
  Metadata to inform the parsing html from twitter.com/search
*/
type ParsingJob struct {
  Html string
}

/*
  Metadata to inform the insertion tweets from twitter.com/search into an SQL table
*/
type InsertJob struct {
  DbEndpoint string
  AwsRegion string
  DbUser string
}

/*
  Metadata to inform the storage of html from twitter.com/search into an S3 bucket
*/
type StorageJob struct {
  Html string
  S3Bucket string
  S3Key string
	S3File string
}

type Tweet map[string]string
type Tweets []Tweet

/*
  Get HTML from twitter.com/search 
*/
func TwitterCrawlJob(j *Job) Job[], error {
	var query strings.Builder

  /*
    TwitterCrawlJob is only implemented to receive jobs of the
    type CrawlingJob, so we catch whether the given job conforms
    to that specification. 
  */
	spec, ok := (*j.Info).(CrawlingJob)
	if !ok {
    err := errors.New("Unable to coerce Job.Info to CrawlingJob")
    return nil, err
	}

	req, err := http.NewRequest("GET", "https://twitter.com/search", nil)
	if err != nil {
    return nil, err
	}

	query.WriteString(spec.Search)

	q := req.URL.Query()
	q.Add("q", url.QueryEscape(query.String()))
	q.Add("src", "typd")
	q.Add("f", "tweets")
	req.URL.RawQuery = q.Encode()

	client := &http.Client{}

	res, err := client.Do(req)
    return nil, err
	}

	bytes, err := ioutil.ReadAll(res.Body)
	if err != nil {
    return nil, err
	}

	html := string(bytes)

	filename.WriteString(time.Now().UTC().Format(time.UnixDate))
	filename.WriteString("-")
	filename.WriteString(req.URL.String())

  /*
    A job specification for uploading html to S3 
  */
	storeHTML := &Job{
		Type: "Store",
		Info: &StorageJob{
			Html: html,
			S3Bucket: os.Getenv("AWS_S3_BUCKET"),
			S3Key: os.Getenv("AWS_S3_KEY"),
			S3File: filename.String(),
		},
	}

  /*
    A job specification for parsing html into json
  */
	parseHtml := &Job{
		Type: "Parse",
		Info: &ParsingJob{ Html: html, },
	}

	jobs := Job[]{ storeHTML, parseHtml }

	return jobs, nil
}

/*
  Parse HTML tweets from twitter.com/serach into json
*/
func TwitterParseJob(j *Job) Job[], error {
  tweets := make(Tweets)

	spec, ok := (*j.Info).(ParsingJob)
	if !ok {
		return nil, error("Unable to coerce Job.Info into ParsingJob")
	}

	bytes := []byte(spec.Html)
  reader := bytes.NewReader(bytes)

	doc, err := goquery.NewDocumentFromReader(reader)
	if err != nil {
    return nil, err
	}

	doc.Find("div.original-tweet").Each(func(i int, s *goquery.Selection) {
    tweet := make(Tweet)

    if id, exists := s.Attr("data-tweet-id"); exists {
      tweet["tweet_id"] = id
    }

    if userID, exists := s.Attr("data-user-id"); exists {
      tweet["user_id"] = userID
    }

    if username, exists := s.Attr("data-name"); exists {
      tweet["user_name"] = username
    }

    if screenname, exists := s.Attr("data-screen-name"); exists {
      tweet["user_handle"] = screenname
    }

    if userLink, exists := s.Find("a.account-group").Attr("href"); exists {
      tweet["user_link"] = userLink
    }


    if permalink, exists := s.Attr("data-permalink-path"); exists {
      tweet["permalink"] = permalink
    }

    if language, exists := s.Find("p.tweet-text").Attr("lang"); exists {
      tweet["language"] = language
    }

    if time, exists := s.Find("a.tweet-timestamp").Attr("title"); exists {
      tweet["time"] = time
    }

    if timestamp, exists := s.Find("span._timestamp").Attr("data-time-ms"); exists {
      tweet["timestamp"] = timestamp
    }


    if retweetCount, exists := s.Find("span.ProfileTweet-action--retweet").Find("span.ProfileTweet-actionCount").Attr("data-tweet-stat-count"); exists {
      tweet["retweets"] = retweetCount
    }

    if favoritesCount, exists := s.Find("span.ProfileTweet-action--favorite").Find("span.ProfileTweet-actionCount").Attr("data-tweet-stat-count"); exists {
      tweet["favorites"] = favoritesCount
    }


    text := make(strings.StringBuilder)

    s.Find("p.tweet-text").Each(func(i int, s *goquery.Selection) {
      if class, exists := s.Attr("class"); exists {
        switch class {
          case "twitter-hashtag" || "tag.twitter-atreply":
            text.WriteString(s.Contents().Text())
            text.WriteString(" ")
          case "twitter-timeline-link":
            if href, exists := s.Attr("href"); exists {
              text.WriteString(href)
            }
          default:
            text.WriteString(s.Text())
            text.WriteString(" ")
        }
      }
    })

    tweet["text"] = text.String()

    tweets = append(tweets, tweet)
	})

	return next, nil
}

/*
  Store unparsed HTML to an AWS S3 Bucket
*/
func TwitterStoreJob(j *Job) *Job[], error {
	return nil
}

/*
  Insert parsed tweets into an AWS RDS SQL table
*/
func TwitterInsertJob(j *job) *Job, error {

}
