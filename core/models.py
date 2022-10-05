from ast import Pass
from unittest.util import _MAX_LENGTH
from xmlrpc.client import DateTime
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
User = get_user_model()

# Create your models here.
class profile(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    id_user= models.IntegerField()
    bio = models.TextField(blank =True)
    prof_img= models.ImageField(upload_to='profile_images',default = 'gitpro.jpg')
    location= models.CharField(max_length=100,blank=True)
   
    def __str__(self):
        return self.user.username
        
class posts(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4)
    user=models.CharField(max_length=100)
    image=models.ImageField(upload_to='post_images')
    caption=models.TextField(max_length=1000)
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)

    def __str__(self):
        return self.user
class likes(models.Model):
    post_id=models.CharField(max_length=500)
    username=models.CharField(max_length=100)

    def __str__(self):
        return self.username
class followerscount(models.Model):
    follower=models.CharField(max_length=100)
    following= models.CharField(max_length=100)
    user=models.CharField(max_length=100)
    
    def __str__(self):
        return self.user
    