from django.contrib import admin
from .models import BlogContext, Comments, UserProfileInfo
# Register your models here.

admin.site.register(BlogContext)
admin.site.register(Comments)
admin.site.register(UserProfileInfo)