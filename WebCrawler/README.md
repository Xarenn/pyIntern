# pyIntern Python2.7
## WebCrawler

Install virtualenv for example: <code>virtualenv -p /usr/bin/python2.7 venv/</code>

Run http server in folder example, command: <code> python3 -m http.server </code>

In script we have BASE_URL variable which is setup to localhost port 8000 we can change it for any other address

## IMPORTANT
If we want to crawl websites not related to start website we must change line:

139 <code>not_crawled = check_urls(tmp_links, keys, url)</code>

to this line:

139 <code>not_crawled = check_urls(tmp_links, keys)</code>
