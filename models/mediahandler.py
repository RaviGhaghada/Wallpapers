import requests
import os
import io
import sys


class MediaHandler:
    """
    A media handler that downloads and stores data in an organized format.

    Attributes:
        self._baddomains    Blacklisted domains
    """

    def __init__(self):
        """
            Creates a directory if it doesn't exist
        """
        try:
            self._path = os.path.expanduser("~") + "/.wallpapers/images"
            print(self._path)
            os.makedirs(self._path)
        except FileExistsError:
            pass
        except Exception as e:
            print(e)
            print("Please create an issue at: https://github.com/RaviGhaghada/Wallpapers")
            sys.exit(-1)

    def is_illegal(self, post) -> bool:
        """
            Returns true if this is a downloadable picture from i.reddit.com
        """
        return "domain" in post and post["domain"] == "i.reddit.com" and not post["is_video"]

    def download_media(self, post) -> str:
        """
        Downloads image from the last post
        obtained via to_next_post / to_previous_post
        """

        if self.is_illegal(post):
            return ""

        # find the right extension for the file
        extension = post["name"] + '.jpg'
        for ext in ('mp4', 'png', 'gif', 'jpeg', 'jpg'):
            if ext in post["url"]:
                extension = "." + ext
                break

        # get media
        r = requests.get(post["url"], stream=True)

        # write media to file
        filename = post["name"] + extension
        with io.open(os.path.join(self._path, filename), 'wb') as file:
            file.write(r.content)
            file.close()

        return filename
