#!/bin/python3
from time import sleep
from time import time
from Extractor import RedditCrawler

def main():
    crawler = RedditCrawler("Eyebleach")

    while True:
        crawler.to_next_post()
        post = crawler.get_post()
        if post["data"]["post_hint"]== "image":
            crawler.download_media()
            sleep(5)
            if input("y?") == "y":
                break


if __name__ == '__main__':
    main()