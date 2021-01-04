from django.db import models
from django.conf import settings
import os
import uuid
import shutil
import glob
from PIL import Image
from .encryption import *


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
######################## End User Unique ID ########################


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
    files_icons = ['.mp3', '.mp4', ".m4v", ".pdf"]
    videos_files = [".mp4", ".m4v", ".mov", ".mkv"]
    img_icon = ['.jpg', '.png']
    file = 'file.svg'
    icons = [
        'audio.svg',
        'video.svg',
        'video.svg',
        'pdf.svg',
    ]

    def __str__(self):
        return str(self.user)

    def trash(self):
        return self.home_dir + "/" + self.uid + "/Trash"

    def create_directory(self, directory):
        try:
            os.chdir(self.current_dir)
            os.mkdir(directory)  # create a directory
        except:
            direc = directory
            counter = 1
            while os.path.exists(directory):# if Dir exists add a number
                directory = direc + str(counter)
                counter += 1     
            os.mkdir(directory)
                    
            

    def move_to_trash(self, source):
        t = self.trash()
        os.chdir(t)
        split_dir = self.current_dir.split("/app/") # split dir to get just the media path
        split_dir = split_dir[1]

        path = os.path.join(split_dir, source)
        movie = Movie.objects.filter(user=self.user)
        for i in movie:
            if i.file_url == path:  # if the file url equals source, delete object
                i.delete()
        p = source
        count = 1
        if os.path.exists(p):# check if trash folder contain folder with the same name
            while os.path.exists(source):
                source = p + str(count)
                count += 1
            os.rename(os.path.join(self.current_dir, p),
                        os.path.join(self.current_dir, source))
            self.move_to_trash(source)
        else:
            if os.path.exists(os.path.join(self.current_dir, "T_" + source)):
                shutil.move(os.path.join(self.current_dir, source), self.trash())
                shutil.move(os.path.join(self.current_dir, "T_" + source), self.trash())
            else:
                shutil.move(os.path.join(
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
        # directories = os.path.join(self.current_dir, open_folder)
        # files = os.listdir(directories)
        # key = load_key(self.get_root())[0]
        # iv= load_key(self.get_root())[1]
        # if files:
        #     for file in files:
        #         decrypt(directories + "/" + file, key, iv)
        #         print(file)
        return os.path.join(self.current_dir, open_folder)

    def go_back(self):
        # files = os.listdir(self.current_dir)
        # key = load_key(self.get_root())[0]
        # iv= load_key(self.get_root())[1]
        # if files:
        #     for file in files:
        #         encrypt(self.current_dir + "/" + file, key)
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
        media = self.current_dir.split("/app/")
        media = media[1]

        return media

    def get_root(self):
        root = self.current_dir.split("/media/")
        root = root[0]

        return root

    # Get folders and files in a dictionary [Name and Icon url]
    def get_f_icon(self, f, icon):
        fs = []
        for i in range(len(f)):
            if f[i].startswith("T_"):
                pass
            else:
                if icon[i] == "":
                    fs.append(
                        {"name": f[i], "url": self.get_media_root() + "/" + f[i], "thumbnail": self.get_media_root() + "/T_" + f[i]})
                elif "." in icon[i]:  # if no thumbnail set file as thumbnail
                    fs.append(
                        {"name": f[i], "url": self.get_media_root() + "/" + f[i], "icon": settings.STATIC_URL + icon[i]})
                else:
                    fs.append(
                        {"name": f[i], "icon": settings.STATIC_URL + icon[i]})
        return fs

    def get_folders_files(self, directories):
        # Set folders and files icons
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

        f_icon = []
        for i in file_extension:  # Check extension and asign an icon else default icon
            if i in self.files_icons:
                f_icon.append("cloud/assets/img/" +
                            self.icons[self.files_icons.index(i)])
            elif i in self.img_icon:
                f_icon.append("")
            else:
                f_icon.append("cloud/assets/img/" + self.file)

        files = self.get_f_icon(folders['files'], f_icon)
      
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
                im.thumbnail((200, 200), Image.ANTIALIAS)
                # don't save if thumbnail already exists
                if infile[0:2] != "T_":
                    # prefix thumbnail file with T_
                    im.save("T_" + infile)

    def rename(self, old_name, new_name):
        filename, file_extension = os.path.splitext(os.path.join(self.current_dir, old_name))
        os.rename(os.path.join(self.current_dir, old_name),
                        os.path.join(self.current_dir, new_name + file_extension))
        print(os.path.exists(os.path.join(self.current_dir, "T_" + old_name)))
        if os.path.exists(os.path.join(self.current_dir, "T_" + old_name)):
            os.rename(os.path.join(self.current_dir, "T_" + old_name),
                            os.path.join(self.current_dir, "T_" + new_name + file_extension))
        
######################## End Cloud model ########################


class Movie(models.Model):
    movie_id = models.CharField(max_length=30, default="")
    title = models.CharField(max_length=255)
    backdrop_path = models.CharField(max_length=500, default="")
    overview = models.CharField(max_length=1000, default="")
    poster_path = models.CharField(max_length=500, default="")
    youtube = models.CharField(
        max_length=500, default="https://www.youtube.com/watch?v=")
    trailer = models.CharField(max_length=500, default="")
    img_url = models.CharField(
        max_length=500, default="https://image.tmdb.org/t/p/original")
    file_url = models.CharField(max_length=500, default="")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def file_name(self):
        file = self.file_url.split("/")
        file = file[-1]
        return file

def user_directory_path(instance, filename):
    user = instance.user
    cloud = Cloud.objects.get(user=user)
    directory = cloud.current_dir
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    return directory + "/"+ filename

class Upload(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to=user_directory_path, max_length=1000)
    uploaded_at = models.DateTimeField(auto_now_add=True)

