package twitter

import (
	"fmt"
	"net/http"
	"net/url"
	"strings"
	"time"
)

const TWITTER_SEARCH_URL = "https://twitter.com/search"

func newTwitterAdvancedSearchRequest(search string, lang string, time time.Time) (*http.Request, error) {
	var query strings.Builder

	req, err := http.NewRequest("GET", TWITTER_SEARCH_URL, nil)
	if err != nil {
		return nil, err
	}

	query.WriteString(search)
	query.WriteString(" since:")

	y, m, d := time.Date()
	date := fmt.Sprintf("%d-%d-%d", y, m, d)
	query.WriteString(date)

	if len(lang) != 0 {
		query.WriteString(" lang:")
		query.WriteString(lang)
	}

	q := req.URL.Query()
	q.Add("q", url.QueryEscape(query.String()))
	q.Add("src", "typd")
	q.Add("f", "tweets")
	req.URL.RawQuery = q.Encode()

	return req, nil
}

func newTwitterSearchRequest(query string) (*http.Request, error) {
	req, err := http.NewRequest("GET", TWITTER_SEARCH_URL, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Add("User-Agent", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0")

	q := req.URL.Query()
	q.Add("q", url.QueryEscape(query))
	q.Add("src", "typd")
	q.Add("f", "tweets")
	req.URL.RawQuery = q.Encode()

	return req, nil
}

func Search(query string) (*http.Response, error) {
	client := &http.Client{}

	req, err := newTwitterSearchRequest(query)
	if err != nil {
		return nil, err
	}

	res, err := client.Do(req)
	if err != nil {
		return nil, err
	}

	return res, nil
}

func AdvancedSearch(search string, lang string, time time.Time) (*http.Response, error) {
	client := &http.Client{}

	req, err := newTwitterAdvancedSearchRequest(search, lang, time)
	if err != nil {
		return nil, err
	}

	res, err := client.Do(req)
	if err != nil {
		return nil, err
	}

	return res, nil
}
