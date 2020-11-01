#!/bin/python3
from time import sleep
from models.crawler import Crawler
from models.mediahandler import MediaHandler
from models.wallsetter import WallSetter

crawler = Crawler("Eyebleach")
handler = MediaHandler()

while True:
    post = crawler.get_post()

    if not handler.is_illegal(post):
        imgpath = handler.download_media(post)
        WallSetter.set_wallpaper(imgpath)

        if input("y?") == "y":
            break

    crawler.to_next_post()
