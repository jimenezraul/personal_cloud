from django.contrib import admin
from .models import UserId, Cloud, Movie, Upload


admin.site.register(UserId)
admin.site.register(Cloud)
admin.site.register(Movie)
admin.site.register(Upload)
