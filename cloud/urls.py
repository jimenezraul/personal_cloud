from django.urls import path, re_path
from . import views
from django.conf.urls import url, include



urlpatterns = [
    path('', views.home_page, name='home'),
    path('open/<str:directory>/', views.open_directory, name='directory'),
    path('go_back_directory/', views.go_back_directory, name='go_back_directory'),
    path('go_back_home/', views.go_back_home, name='go_back_home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete/<str:name>/', views.delete_item, name='delete'),
    path('create/', views.create_folder, name='create_folder'),
]