import os
import shutil
import uuid
from django.conf import settings


class Cloud:
    def __init__(self):
        self.current_dir = ""  # current directory
        self.home_dir = settings.MEDIA_ROOT + "/cloud"  # home directory
        self.user_root = ""
        self.user_id = ""
        self.dir_name = ""
        self.trash = '/Users/Trash'
        self.unwanted_files = ('.download',)
        self.files_icons = ['.mp3', '.mp4']
        self.img_icon = ['.jpg', '.png', '.pdf']
        self.file = 'file.svg'
        self.icons = [
            'picture.svg',
            'picture.svg',
            'audio.svg',
            'video.svg',
            'pdf.svg',
        ]

    def create_directory(self, directory):
        os.mkdir(directory)  # create a directory
        directory = os.getcwd()
        return os.path.join(self.current_dir, directory)

    # def current_path(self, directory):
    #     self.current_dir = directory

    def move_to_trash(self, source):
        destination = shutil.move(source, self.trash)
        return destination

    def go_back_home(self):
        return self.home_dir

    def empty_trash(self):
        for filename in os.listdir(self.trash):
            file_path = os.path.join(self.trash, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def open_directory(self, open_folder):
        return os.path.join(self.current_dir, open_folder)

    def go_back(self):
        current_path = self.current_dir.split("/")  # split current directory
        current_path.pop()  # last string deleted from split
        if current_path:
            self.dir_name = current_path[-1]

        if self.current_dir == self.home_dir:
            current_path = self.home_dir
        else:
            # join the split back together
            current_path = "/".join(current_path)
        return current_path

    def get_media_root(self):
        media = self.current_dir.split("/personal_cloud/")
        media = media[1]

        return media

    def get_f_icon(self, f, icon):  # Get folders and files in a dictionary [Name and Icon url]
        fs = []
        for i in range(len(f)):
            if icon[i] == "":
                fs.append(
                    {"name": f[i], "icon": self.get_media_root() + "/" + f[i]})
            else:
                fs.append(
                    {"name": f[i], "icon": settings.STATIC_URL + icon[i]})
        return fs

    def get_folders_files(self, directories):  # Set folders and files icons
        folders = {
            "folders": [i for i in directories if "." not in i],
            # list of all directories in current path
            "files": [i for i in directories if "." in i and not i.startswith(".") and not i.endswith(
                self.unwanted_files)]
        }  # list of all files in directory

        icon = []
        for i in folders['folders']:
            if i == "Trash":
                icon.append('cloud/assets/img/trash.svg')
            else:
                icon.append('cloud/assets/img/folder.svg')

        folder = self.get_f_icon(folders['folders'], icon)

        # List the files extension in the directory
        file_extension = [os.path.splitext(i)[1] for i in folders["files"]]

        icon = []
        for i in file_extension:  # Check extension and asign an icon else default icon
            if i in self.files_icons:
                icon.append(self.icons[self.files_icons.index(i)])
            if i in self.img_icon:
                icon.append("")
            else:
                icon.append("cloud/assets/img/" + self.file)

        files = self.get_f_icon(folders['files'], icon)
        return files, folder
