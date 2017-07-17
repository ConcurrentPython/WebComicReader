import aiohttp
import asyncio
import feedparser
from pathlib import Path
import socket
import webbrowser

async def latest_comic(rss_feed):
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(rss_feed) as resp:
                text = await resp.read() if resp.status == 200 else None
    except Exception as e:
        print(e)
        print("BAD URL %s" % e)
        return

    if text:
        rss = feedparser.parse(text)
        entries = rss.get('entries')
        if entries:
            guid = entries[0].get('guid', "")
            if guid.startswith("http"):
                return guid

async def good_latest_comic(rss_url):
    guid = await latest_comic(rss_url)
    if guid:
        async with aiohttp.ClientSession() as client:
            async with client.head(guid) as resp:
                if resp.status < 400:
                    print(guid)
                    return guid


def open_list(rss_list):
    loop = asyncio.get_event_loop()
    to_do = [good_latest_comic(rss_url) for rss_url in rss_list]
    res, _ = loop.run_until_complete(asyncio.wait(to_do))
    loop.close()
    return res

if __name__ == '__main__':
    from time import time
    t0 = time()
    rss_list = (Path.cwd() / "good.txt").read_text().splitlines()
    open_list(rss_list[:20])
    print('Elapsed time:', time() - t0)
