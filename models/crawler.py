import requests
import os


class Crawler:
    """
    A web crawler that crawls a given subreddit and lets us access each post.

    Attributes:
        self._url      URL of the reddit page
        self._header   Dictionary of HTTP Headers to send with the request
        self._data     Holds data derived from requests
        self._counter  Counter to keep track of post index
        self._page     Index of the current page (as if it's loaded in reddit)
    """

    def __init__(self, subredditname):
        """
        Constructor of a subreddit crawler
        :param subredditname: Name of the subreddit to crawl
        """
        self._url = 'https://reddit.com/r/{}/.json?sort=top'.format(
            subredditname)
        self._header = {
            'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'Mozilla/5.0'))}

        self._data = None
        self._pagedata = None

        self._counter = 0
        self._page = 0

        self._refresh()

    def _refresh(self, pageinfo="") -> None:
        """
        Request new set of data and insert it into self._data
        :param pageinfo: additional information about the page such as page number
        """
        response = requests.get(self._url + pageinfo,
                                headers=self._header).json()

        self._data = response['data']['children']

        self._pagedata = {
            "after": response["data"]["after"],
            "before": response["data"]["before"]
        }

        self._counter = 0
        while self._data[self._counter]['data']['stickied']:
            self._counter += 1

    def to_next_post(self) -> None:
        """
        Increase the counter and get the next available post
        :return: post found at next index
        """
        self._counter += 1

        if self._counter >= len(self._data):
            # shift to the next page
            self._page += 1
            pageinfo = "count={}&after={}".format(
                25*self._page, self._pagedata['after'])
            self._refresh(pageinfo)

    def to_previous_post(self) -> None:
        """
        Decrease the counter and get the previous available post
        :return: post found at previous index
        """
        self._counter -= 1

        if self._counter < 0:
            if self._page == 0:
                self._counter = 0
            else:
                # shift to previous page
                self._page -= 1
                if self._page == 1:
                    pageinfo = ""
                else:
                    pageinfo = "count={}&before={}".format(
                        25*self._page, self._pagedata['before'])
                self._refresh(pageinfo)

    def get_post(self) -> dict:
        return self._data[self._counter]["data"]
