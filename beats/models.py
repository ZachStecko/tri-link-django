from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os
from django.utils.timezone import now

class BeatVideo(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(default='Default Value')
    premium = models.BooleanField(default=True)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripeid = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)
    terms_confirmed = models.BooleanField(default=False)
    video_count = models.IntegerField(default=0)
    created = models.DateTimeField(editable=True ,default=now)
    total_count =  models.IntegerField(default=0)
    random_id = models.CharField(max_length=10, default='xxxxxxxxxx')
    
    def __str__(self):
        return str(self.user)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'Audio/user_{0}/{1}'.format(instance.user.id, filename)

class Document(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='document_name',on_delete=models.CASCADE)
    docfile = models.FileField(upload_to=user_directory_path)
    imgfile = models.FileField(upload_to=user_directory_path)

class Count(models.Model):
    total = models.IntegerField(default=0)