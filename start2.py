import feedparser
import requests
from pathlib import Path
import socket
import webbrowser

rss_list = (Path.cwd() / "good.txt").read_text().splitlines()

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

for rss in rss_list[:7]:
    latest = latest_comic(rss)
    print(latest)
    webbrowser.open_new_tab(latest)
