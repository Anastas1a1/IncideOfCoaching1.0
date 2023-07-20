from django.db import models
from django.contrib.auth.models import User


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tg_id = models.IntegerField(unique=True)


class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    tg_id = models.IntegerField(unique=True)


class Subscription(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    subscription_date = models.DateField(null=True, blank=True)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=10)


class File(models.Model):
    year = models.CharField(max_length=4)
    category = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    title = models.CharField(max_length=255)


class FileGoogle(models.Model):
    file = models.OneToOneField(
        File, on_delete=models.CASCADE, related_name='files_google')
    google_id = models.CharField(max_length=40)
    link = models.TextField()


class FileTg(models.Model):
    file = models.OneToOneField(
        File, on_delete=models.CASCADE, related_name='files_tg')
    tg_id = models.CharField(max_length=100)
    ext = models.CharField(max_length=40)
