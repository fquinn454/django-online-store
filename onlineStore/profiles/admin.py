from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, ProductSet

admin.site.register(Profile)
admin.site.register(ProductSet)

