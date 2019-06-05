import requests
import glob
import os
from io import open as iopen

class RedditCrawler:
    """
    A web crawler that crawls a given subreddit and lets us access each post.
    It can also download media.

    Attributes:
        self.__url      URL of the reddit page
        self.__header   Dictionary of HTTP Headers to send with the request
        self.__data     Holds data derived from requests
        self.__counter  Counter to keep track of post index
        self.__page     Index of the current page (as if it's loaded in reddit)
    """

    def __init__(self, subredditname):
        """
        Constructor of a subreddit crawler
        :param subredditname: Name of the subreddit to crawl
        """
        self.__url = 'https://reddit.com/r/{}/.json?sort=top'.format(subredditname)
        self.__header = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'Mozilla/5.0'))}

        self.__data = None

        self.__counter = -1
        self.__page = 0

        self.refresh()


    def refresh(self, pageinfo=""):
        """
        Request new set of data and insert it into self.__data
        :param pageinfo: additional information about the page such as page number
        """
        self.__data = requests.get(self.__url + pageinfo, headers=self.__header).json()

        self.__data = self.__data['data']['children']
        i=0
        while i < len(self.__data):
            if self.__data[i]['data']['stickied']:
                del self.__data[i]
            else:
                i+=1

        self.__counter = -1

    def to_next_post(self):
        """
        Increase the counter and get the next available post
        :return: post found at next index
        """
        self.__counter += 1

        # TODO Allow shifting to the next page

        # temporarily: loops the end back to the front
        if self.__counter > len(self.__data):
            self.__counter=0

        return self.__data[self.__counter]

    def to_previous_post(self):
        """
        Decrease the counter and get the previous available post
        :return: post found at previous index
        """
        self.__counter -= 1

        # TODO allow shifting to the previous page

        # temporarily: loops the start back to the end
        if self.__counter < 0:
            self.__counter = len(self.__data)-1

        return self.__data[self.__counter]


    # Most of the code comes from
    def download_media(self):
        """
        Downloads image/gif from the last post
        obtained via to_next_post / to_previous_post
        """

        # in case this method is called right after refresh() or initialization
        if self.__counter==-1:
            print("Please call either to_next_post or to_previous_post "
                  + "to move the counter to a non-negative post")
            return

        # obtain the domain and url of post to be downloaded
        post = self.__data[self.__counter]['data']
        domain = post['domain']
        url = post['url']

        # reject text posts for now
        if domain.startswith("self."):
            print("Failure: Post is a text post")
            return

        # reject v.redd.it videos
        elif domain == "v.redd.it":
            print("Failure: v.redd.it doesn't let users download videos")
            return

        # accept gfycat videos
        elif domain == "gfycat.com":
            gfy_url = url.split('/')[-1]
            r = requests.get("https://api.gfycat.com/v1/gfycats/{}".format(gfy_url)).json()
            mediaurl = r['gfyItem']['mp4Url']

        # mp4 is better for storing gifs
        elif domain == "i.imgur.com":
            mediaurl = url.replace('.gifv', 'mp4')

        # example: image from i.redd.it
        else:
            mediaurl = url

        # find the right extension for the file
        extension = '.jpg'
        for ext in ('mp4', 'png', 'gif', 'jpeg', 'jpg'):
            if ext in mediaurl:
                extension = "." + ext

        # remove former file(s)
        for cat_file in glob.glob("ex"):
            os.unlink(cat_file)

        # get media
        r = requests.get(mediaurl, stream=True)

        # write media to file
        fname = 'ex' + extension
        with iopen(fname, 'wb') as file:
            file.write(r.content)
            file.close()






