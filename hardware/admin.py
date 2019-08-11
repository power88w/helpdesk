from django.contrib import admin
from .models import BlogPost,BlogComment,BlogStats
# Register your models here.

admin.site.register(BlogPost)
admin.site.register(BlogComment)
admin.site.register(BlogStats)