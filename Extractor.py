import requests
import os

class RedditCrawler:

    def __init__(self, subredditname):
        self.__url = 'https://reddit.com/r/{}/.json?sort=top'.format(subredditname)
        self.__header = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'Mozilla/5.0'))}

        self.__data = None

        self.__counter = -1
        self.__page = 0

        self.refresh()


    def refresh(self, pageinfo=""):
        self.__data = requests.get(self.__url + pageinfo, headers=self.__header).json()

        self.__data = self.__data['data']['children']

        i=0
        while i < len(self.__data):
            if self.__data[i]['data']['stickied']:
                del self.__data[i]
            else:
                i+=1

        self.__counter = -1

    def get_next_post(self):
        self.__counter += 1

        # TODO Allow shifting to the next page

        if self.__counter < len(self.__data):
            return self.__data[self.__counter]
        else:
            self.__counter=0
            return self.__data[self.__counter]

    def get_previous_post(self):
        self.__counter -= 1

        # TODO allow shifting to the previous page

        if self.__counter >= 0:
            return self.__data[self.__counter]
        else:
            self.__counter = len(self.__data)-1
            return self.__data[self.__counter]