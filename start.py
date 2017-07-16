import feedparser
import requests
from pathlib import Path
import socket

rss_list = (Path.cwd() / "urls.txt").read_text().splitlines()

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

with open("good.txt", 'w') as good:
    for rss in rss_list:
        latest = latest_comic(rss)
        if latest:
            print(latest)
            good.write(rss + "\n")
