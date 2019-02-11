"""
    Global values
    browser - instance of mechanicalsoup framework browser
    links_data - variable to storing data from links
    bad_codes - http status codes to prevent unnecessary parsing
"""

from urlparse import urlparse
import json
import mechanicalsoup
import requests


links_data = []
browser = mechanicalsoup.StatefulBrowser()
bad_codes = [404, 409, 400, 403, 401, 501, 500]
BASE_URL = "http://localhost:8000"


class DataSite:
    """
        DataSite class it's a simple structure to storing information about website and to serialize it
    """

    def __init__(self, title, links):
        self.title = title
        self.links = links

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)


def get_data_url(url):
    """
        get_data_url(url) method which parse and provides additional links from current page

        :url - url type String which should be prefixed by http or https
    """

    global links_data

    url_parser = urlparse(url)
    try:
        status_code = browser.open(url).status_code

        if status_code in bad_codes:
            return []

    except (requests.exceptions.ConnectionError,
            requests.exceptions.InvalidURL,
            requests.exceptions.InvalidSchema) as exc:
        print "Invalid request or url: " + str(exc)
        return None

    links = []
    for link in browser.links():
        target = link.attrs['href']
        if target.startswith('http'):
            links.append(target)
        else:
            if target.startswith('/'):
                links.append('http://'+url_parser.netloc+target)
            else:
                links.append('http://'+url_parser.netloc+'/'+target)

    try:
        title = browser.get_current_page().find('title').text
    except AttributeError as exc:
        print "Attribute error: " + str(exc)
        title = "None"

    site_data = str(DataSite(title, links))
    try:
        keys = [link.keys()[0] for link in links_data]

        if url in keys:
            return []

        else:
            links_data.append({url: site_data})
            to_do_links = [link_s for link_s in links if (link_s in keys) is False]
            return to_do_links

    except IndexError:
        print "Invalid dictionary"
        return None


def check_urls(urls, keys, base_url=None):
    """
        check_urls(urls, keys)
        Checking urls which we crawled or not
        base_url check that, we want to crawl other websites not related to base website.

        for example we have base_url as localhost and we got google website from links,
            if base_url is None, script will crawl google too.


        :urls - list of urls which were indexed or not
        :keys - list of keys from links_data dictionaries
        :base_url - start url
        return list of urls which weren't crawled
    """

    not_crawled = [url for url in urls if url not in keys]
    if base_url is None:
        return not_crawled
    else:
        url_parser = urlparse(base_url)
        not_crawled_within = [url for url in not_crawled if url_parser.netloc == urlparse(url).netloc]

        return not_crawled_within


def site_map(url):
    """
        site_map(url)
        Main method allows to crawling websites

        :url - address to website in type String should be prefixed 'http' or 'https'
    """

    links = get_data_url(url)

    if links is None or len(links) == 0:
        return

    tmp_links = set()
    while True:
        for link in links:
            crawled = get_data_url(link)
            if crawled is not None and len(crawled) > 0:
                for crawl in crawled:
                    tmp_links.add(crawl)
            else:
                continue
        try:
            keys = [link.keys()[0] for link in links_data]
            not_crawled = check_urls(tmp_links, keys, url)

            if len(not_crawled) > 0:
                links = not_crawled
            else:
                break
        except IndexError:
            print "Invalid dictionary"


""" Execution """

try:
    site_map(BASE_URL)
    print(json.dumps(links_data))

except KeyboardInterrupt:
    print(json.dumps(links_data))
