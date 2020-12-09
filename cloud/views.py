from django.shortcuts import render, redirect
from django.conf import settings
from .models import UserId, Cloud
import os
# from .cloud import Cloud
import shutil
import socket
import platform
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home_page(request):
    try:
        user = request.user
        cloud = Cloud.objects.filter(user=user)
        database = UserId.objects.filter(user=user)
        if len(cloud) == 0:
            new_user = Cloud(user=user)
            new_user.save()
            return redirect('home')
        else:
            cloud = cloud[0]

        # If user don't have a unique id, set one and create a home dir
        if len(database) == 0:
            query = UserId(user=user)  # create user id
            query.save()  # save user id
            # default folders in home directory
            directories = ["Documents", "Music", "Pictures", "Videos", "Trash"]
            database = UserId.objects.filter(
                user=user)  # user id in the database
            uid = str(database[0])  # set a variable to user id
            os.chdir(cloud.home_dir)  # change directory to the root directory
            os.mkdir(uid, mode=0o775)  # create a dir with the user id
            # set home directory to the id folder created
            user_dir = os.path.join(cloud.home_dir, uid)
            # create a cloud associated with user
            instance = Cloud.objects.get(user=user)
            instance.current_dir = user_dir  # set the current folder to the home directory
            instance.save()  # save the changes
            os.chdir(user_dir)  # change directory to home directory
            for i in directories:
                os.mkdir(i, mode=0o775)  # create default folders
            return redirect('home')
        else:# if id and home directory are created this will run instead
            uid = str(database[0])# select user id
            cloud.user_root = os.path.join(cloud.home_dir, uid)# join root dir and id dir
            root = cloud.user_root# set root dir to the join link above
            if uid not in cloud.current_dir.split("/"): # if id not in current dir
                cloud.current_dir = root# set current dir to user root dir

        instance = Cloud.objects.get(user=user)
        instance.current_dir = cloud.current_dir
        instance.uid = uid
        instance.save()
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        total, used, free = shutil.disk_usage(cloud.home_dir)
        total = total // (2 ** 30)
        used = used // (2 ** 30)
        free = free // (2 ** 30)

        os.chdir(cloud.current_dir)
        directories = os.listdir(cloud.current_dir)

        folders = cloud.get_folders_files(directories)
        files = folders[0]
        folders = folders[1]

        if os.getcwd() == root:
            back = True
        else:
            back = False
        percent = int((used / total) * 100)
        media = cloud.get_media_root()
        trash = cloud.trash()
        trash_count = len([name for name in os.listdir(trash)])
        
        context = {
            "folders": folders,
            "files": files,
            "user": user,
            "back": back,
            "dir_name": cloud.dir_name,
            "total": total,
            "used": used,
            "percent": percent,
            "ip": IPAddr,
            "hostname": hostname,
            "current_path": media,
            "trash_count": trash_count,
        }
        return render(request, "cloud/index.html", context)
    except BaseException as e:
        print(e)
        user = request.user
        cloud = Cloud.objects.filter(user=user)[0]
        n_dir = cloud.dir_name
        p_dir = cloud.go_back()
        p_dir = p_dir.split("/")
        p_dir.pop()
        p_dir = "/".join(p_dir)
        current_dir = os.path.join(p_dir, n_dir)
        instance = Cloud.objects.get(user=user)
        instance.current_dir = current_dir
        instance.dir_name = n_dir
        instance.save()
        return redirect("home")


def go_back_directory(request):
    user = request.user
    cloud = Cloud.objects.filter(user=user)[0]
    back = cloud.go_back()
    cloud.dir_save()
    instance = Cloud.objects.get(user=user)
    instance.current_dir = back
    instance.save()
    return redirect("home")


def go_back_home(request):
    user = request.user
    database = str(UserId.objects.filter(user=user)[0])
    cloud = Cloud.objects.filter(user=user)[0]
    back_home = settings.MEDIA_ROOT + "/cloud" + database
    instance = Cloud.objects.get(user=user)
    instance.current_dir = back_home
    instance.save()
    return redirect("home")


def open_directory(request, directory):
    user = request.user
    cloud = Cloud.objects.filter(user=user)[0]
    direc = cloud.open_directory(directory)
    instance = Cloud.objects.get(user=user)
    instance.current_dir = direc
    instance.dir_name = directory
    instance.save()
    return redirect("home")


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'username or password is not correct')
                return redirect(request.POST.get('next'))
        except:
            return redirect('/')

    context = {

    }
    return render(request, "cloud/login.html", context)


def logout_view(request):
    user = request.user
    cloud = Cloud.objects.filter(user=user)[0]
    instance = Cloud.objects.get(user=user)
    instance.current_dir = cloud.home_dir
    instance.save()
    logout(request)
    return redirect('login')

def delete_item(request, name):
    cloud = Cloud.objects.filter(user=request.user)[0]
    cloud.move_to_trash(name)
    return redirect('home')

def create_folder(request):
    cloud = Cloud.objects.filter(user=request.user)[0]
    if request.method == 'POST':
        folder = request.POST.get('folder')
        cloud.create_directory(folder)

    return redirect("home")