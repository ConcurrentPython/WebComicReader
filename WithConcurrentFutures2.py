import feedparser
import requests
from pathlib import Path
import socket
import webbrowser
import concurrent.futures

def latest_comic(rss_feed):
    try:
        r = requests.get(rss_feed)
    except Exception as e:
        print(e)
        print(f"BAD URL {rss_feed}")
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
    if requests.head(latest).status_code < 400:
        return latest


def open_list(rss_list):
    bob = concurrent.futures.ThreadPoolExecutor()
    guids = bob.map(latest_good_comic, rss_list)
    for latest in guids:
        if latest:
            print(latest)
            webbrowser.open_new_tab(latest)


if __name__ == '__main__':
    from time import time
    t0 = time()
    rss_list = (Path.cwd() / "good.txt").read_text().splitlines()
    open_list(rss_list[:20])
    print('Elapsed time:', time() - t0)
