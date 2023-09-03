import requests
from bs4 import BeautifulSoup
from threading import Thread
from typing import Callable
import time

from ApkMirrorParser import downloadFromApkMirror
from logger import listener_logger

YOUTUBE_RSS_URL = "http://www.apkmirror.com/apk/google-inc/youtube/variant-%7B%22minapi_slug%22%3A%22minapi-26%22%7D/feed/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class ReleaseListener:
    def __init__(self, rss_url: str, release_callback: Callable[[str], any], check_interval=15*60):
        self.release_callback = release_callback
        self.rss_url = rss_url
        self.soup = None
        self.check_interval = check_interval
        Thread(target=self._listenerThread).start()

    def _listenerThread(self):
        current_release = ""
        old_release = ""
        while True:
            current_release = self._getNewestRelease()
            if current_release != old_release:
                listener_logger.info(f"New release {current_release} found! Calling callback function")
                self.release_callback(current_release)
                old_release = current_release
            else:
                listener_logger.info(f"No new releases found. Newest is: {current_release}")
            time.sleep(self.check_interval)

    def _getNewestRelease(self):
        self._scanForReleases()
        return self._getReleases()[0]

    def _scanForReleases(self):
        repl = requests.get(self.rss_url, headers=headers)
        self.soup = BeautifulSoup(repl.content, "xml")

    def _getReleases(self):
        return [item.link.text for item in self.soup.find_all("item")]

if __name__ == "__main__":
    yt_listener = ReleaseListener(YOUTUBE_RSS_URL, downloadFromApkMirror)