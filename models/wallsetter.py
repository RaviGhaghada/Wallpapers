import os


class WallSetter:

    @staticmethod
    def set_wallpaper(path):
        print("Path", path)
        cmd = "gsettings set org.mate.background picture-filename " + path
        print(cmd)
        os.system(cmd)
