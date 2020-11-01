#!/bin/python3
from time import sleep
from models.crawler import Crawler
from models.mediahandler import MediaHandler


def main():
    crawler = Crawler("Eyebleach")
    handler = MediaHandler()
    while True:
        crawler.to_next_post()
        post = crawler.get_post()
        filepath = handler.download_media(post)
        print(filepath)
        if input("y?") == "y":
            break


if __name__ == '__main__':
    main()
