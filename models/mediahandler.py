from models.wallmanager import WallManager
import requests
import os
import io
import sys
from models.wallmanager import WallManager


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
            os.makedirs(self._path)

            self._initialpath = WallManager.get_wallpaper_path()

            if self._initialpath == "":
                # gsettings will not accept empty paths
                self._initialpath = "0"

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
        ispicture = post["url"].endswith(".jpg") or post["url"].endswith(
            ".png") or post["url"].endswith(".jpeg")

        return not ispicture

    def download_media(self, post) -> str:
        """
        Downloads image from post object and returns filepath to image
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
        imgpath = os.path.join(self._path, filename)

        with io.open(imgpath, 'wb') as file:
            file.write(r.content)
            file.close()

#        print("> " + post["name"] + " > " + post["url"] + " > " + extension)
        return imgpath

    def get_initial_path(self):
        return self._initialpath
