from django.contrib import admin
from .models import UserId, Cloud, Movie


admin.site.register(UserId)
admin.site.register(Cloud)
admin.site.register(Movie)