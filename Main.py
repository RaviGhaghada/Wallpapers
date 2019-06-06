#!/bin/python3

from Extractor import RedditCrawler

def main():
    crawler = RedditCrawler("Eyebleach")

    while True:
        post = crawler.to_next_post()
        if post["data"]["post_hint"]== "image":
            crawler.download_media()
            break

if __name__ == '__main__':
    main()