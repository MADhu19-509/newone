from django.contrib import admin
from .models import likes, profile,posts,likes,followerscount
# Register your models here.
admin.site.register(profile)
admin.site.register(posts)
admin.site.register(likes)
admin.site.register(followerscount)