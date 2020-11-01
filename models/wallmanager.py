import os


class WallManager:
    """
    A static class that has a set of function to interact with the OS's wallpaper
    """

    @staticmethod
    def get_wallpaper_path() -> str:
        """
        Obtain the current wallpaper
        """
        cmd = "gettings get org.mate.background picture-filename "
        imgpath = os.system(cmd)
        return imgpath

    @staticmethod
    def set_wallpaper(imgpath: str) -> None:
        """
        Set the wallpaper to the current one
        """
        cmd = "gsettings set org.mate.background picture-filename " + imgpath
        os.system(cmd)
