#!/bin/python3
import argparse
from models import Crawler, MediaHandler, WallManager


def main():

    parser = argparse.ArgumentParser(
        description='Python library that fetches pictures from a given subreddit'
    )

    required = parser.add_argument_group('required arguments')
    required.add_argument('-s', '-subreddit', dest='subreddit',
                          type=str, required=True, help='name of subreddit')

    arguments = parser.parse_args()

    crawler = Crawler(arguments.subreddit)
    handler = MediaHandler()

    try:
        while True:
            post = crawler.get_post()

            if not handler.is_illegal(post):
                imgpath = handler.download_media(post)
                WallManager.set_wallpaper(imgpath)

                if input("y?") == "y":
                    break

            crawler.to_next_post()

    except SystemExit as e:
        if e.code != 0:
            # reset wallpaper to what it was before
            WallManager.set_wallpaper(handler.get_initial_path())


if __name__ == "__main__":
    main()
