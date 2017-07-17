import feedparser
import requests.async
from pathlib import Path
import socket
import webbrowser
import gevent
import gevent.event

def request(method, url):
    event = gevent.event.Event()
    result = None
    def response(response):
        nonlocal result
        result = response
        event.set()

    getattr(requests.async, method)(url, hooks=dict(response=response)).send()
    event.wait()
    return result[0]

def latest_comic(rss_feed):
    try:
        r = request('get', rss_feed)
    except Exception as e:
        print(e)
        print("BAD URL %s" % e)
        return

    if r.status_code != 200:
        return
    rss = feedparser.parse(r.text)
    entries = rss.get('entries')
    if entries:
        guid = entries[0].get('guid', "")
        if guid.startswith("http"):
            return guid


def latest_good_comic(rss_feed):
    latest = latest_comic(rss_feed)
    if request('head', latest).status_code < 400:
        return latest


def open_list(rss_list):
    jobs = [gevent.spawn(latest_good_comic, rss_url) for rss_url in rss_list]
    gevent.joinall(jobs)
    print([job.value for job in jobs])
    print(len([job.value for job in jobs if job.value]))

if __name__ == '__main__':
    from time import time
    t0 = time()
    rss_list = (Path.cwd() / "good.txt").read_text().splitlines()
    open_list(rss_list[:20])
    print('Elapsed time:', time() - t0)
