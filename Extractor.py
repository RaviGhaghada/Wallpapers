import requests
import glob
import os
from io import open as iopen

class RedditCrawler:

    def __init__(self, subredditname):
        self.__url = 'https://reddit.com/r/{}/.json?sort=top'.format(subredditname)
        self.__header = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'Mozilla/5.0'))}

        self.__data = None
        self.__current = None

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

    def to_next_post(self):
        self.__counter += 1

        # TODO Allow shifting to the next page

        if self.__counter > len(self.__data):
            self.__counter=0

        return self.__data[self.__counter]

    def to_previous_post(self):
        self.__counter -= 1

        # TODO allow shifting to the previous page

        if self.__counter < 0:
            self.__counter = len(self.__data)-1

        return self.__data[self.__counter]


    def download_media(self):

        post = self.__data[self.__counter]['data']
        domain = post['domain']
        url = post['url']
        
        if domain.startswith("self."):
            print("Failure: Post is a text post")
            return None, None

        elif domain == "v.redd.it":
            print("Failure: v.redd.it doesn't let users download videos")
            return None, None

        if domain == "gfycat.com":
            gfy_url = url.split('/')[-1]
            r = requests.get("https://api.gfycat.com/v1/gfycats/{}".format(gfy_url)).json()
            mediaurl = r['gfyItem']['mp4Url']
        elif domain == "i.imgur.com":
            mediaurl = url.replace('.gifv', 'mp4')
        else:
            mediaurl = url

        extension = '.jpg'
        for ext in ('mp4', 'png', 'gif', 'jpeg', 'jpg'):
            if ext in mediaurl:
                extension = "." + ext

        # remove former file
        for cat_file in glob.glob("*"):
            os.unlink(cat_file)

        fname = 'cat' + extension
        r = requests.get(mediaurl, stream=True)

        with iopen(fname, 'wb') as file:
            file.write(r.content)
            file.close()






