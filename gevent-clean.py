import feedparser
from pathlib import Path
import webbrowser
import gevent
import geventhttpclient

from geventhttpclient import HTTPClient
from geventhttpclient.url import URL

def request(method, url, level=0):
    url = URL(url)
    http = HTTPClient.from_url(url, concurrency=10)
    response = getattr(http, method)(url.request_uri)
    if response.status_code in (301, 302) and level < 3:
        [loc] = [v for n, v in response.headers if n.lower() == 'location']
        return request(method, loc, level+1)

    result = response.status_code, response.read()
    http.close()
    return result

def latest_comic(rss_feed):
    try:
        status, body = request('get', rss_feed)
    except Exception as e:
        print(e)
        print("BAD URL %s" % e)
        return

    if status != 200:
        print('BAD STATUS', status, rss_feed)
        return
    rss = feedparser.parse(body)
    entries = rss.get('entries')
    if entries:
        guid = entries[0].get('guid', "")
        if guid.startswith("http"):
            return guid


def latest_good_comic(rss_feed):
    latest = latest_comic(rss_feed)
    try:
        if request('head', latest)[0] < 400:
            return latest
    except Exception:
        pass

def open_list(rss_list):
    jobs = [gevent.spawn(latest_good_comic, rss_url) for rss_url in rss_list]
    gevent.joinall(jobs)
    print([job.value for job in jobs])

if __name__ == '__main__':
    from time import time
    t0 = time()
    rss_list = (Path.cwd() / "good.txt").read_text().splitlines()
    open_list(rss_list[:20])
    print('Elapsed time:', time() - t0)
