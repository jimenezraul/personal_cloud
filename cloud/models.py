from django.db import models
from django.conf import settings
import os
import uuid
import shutil
import glob
from PIL import Image


######################## User Unique ID ########################
class UserId(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=True,
        unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


######################## Cloud model ########################
class Cloud(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    current_dir = models.CharField(max_length=1000, default="")
    uid = models.CharField(max_length=1000, default="")
    dir_name = models.CharField(max_length=1000, default="")
    home_dir = settings.MEDIA_ROOT + "/cloud"
    user_root = models.CharField(max_length=1000, default="")
    unwanted_files = ('.download',)
    files_icons = ['.mp3', '.mp4']
    img_icon = ['.jpg', '.png']
    file = 'file.svg'
    icons = [
        'picture.svg',
        'picture.svg',
        'audio.svg',
        'video.svg',
        'pdf.svg',
    ]

    def __str__(self):
        return str(self.user)

    def trash(self):
        return self.home_dir + "/" + self.uid + "/Trash"

    def create_directory(self, directory):
        os.chdir(self.current_dir)
        os.mkdir(directory)  # create a directory

    def move_to_trash(self, source):
        t = self.trash()
        os.chdir(t)
        if os.path.exists(source):
            os.rename(os.path.join(self.current_dir, source),
                      os.path.join(self.current_dir, source + "1"))
            source = source + "1"
            self.move_to_trash(source)
        else:
            destination = shutil.move(os.path.join(
                self.current_dir, source), self.trash())

    def go_back_home(self):
        return self.home_dir

    def empty_trash(self):
        for filename in os.listdir(self.trash()):
            file_path = os.path.join(self.trash(), filename)
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

    # Get folders and files in a dictionary [Name and Icon url]
    def get_f_icon(self, f, icon):
        fs = []
        for i in range(len(f)):
            if f[i].startswith("T_"):
                pass
            else:
                if icon[i] == "":
                    fs.append(
                        {"name": f[i], "icon": self.get_media_root() + "/" + f[i], "thumbnail": self.get_media_root() + "/T_" + f[i]})
                elif "." in f[i]:  # if no thumbnail set file as thumbnail
                    fs.append(
                        {"name": f[i], "icon": self.get_media_root() + "/" + f[i], "thumbnail": self.get_media_root() + "/" + f[i]})
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

    def dir_save(self, *args, **kwargs):
        try:
            name = Cloud.objects.get(user=self.user)
            name.dir_name.save()
        except:
            pass
        super(Cloud, self).save(*args, **kwargs)

    def get_thumbnail(self):
        for i in self.img_icon:
            # get all the jpg files from the current folder
            for infile in glob.glob("*"+i):
                im = Image.open(infile)
                # convert to thumbnail image
                im.thumbnail((128, 128), Image.ANTIALIAS)
                # don't save if thumbnail already exists
                if infile[0:2] != "T_":
                    # prefix thumbnail file with T_
                    im.save("T_" + infile)
