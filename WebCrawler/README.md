# pyIntern Python2.7
## WebCrawler
if you don't have virtualenv so use pip install -r requirements.txt for installing it globally

Create virtualenv: <code>python -m virtualenv venv</code>

Install virtualenv for example: <code>virtualenv -p /usr/bin/python2.7 venv/</code>

Run http server in folder example, command: <code> python3 -m http.server </code>

In script we have BASE_URL variable which is setup to localhost port 8000 we can change it for any other address

## How to run it?

Use: <code>python web_crawler.py</code>

## IMPORTANT
If we want to crawl websites not related to start website we must change line:

139 <code>not_crawled = check_urls(tmp_links, keys, url)</code>

to this line:

139 <code>not_crawled = check_urls(tmp_links, keys)</code>

## Output
While script is still working we can end the program using CTRL+Z or CTRL+C and we should see data on the standard output or if script ends output will be in the console.
