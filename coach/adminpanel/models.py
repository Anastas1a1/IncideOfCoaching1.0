from django.db import models
from django.contrib.auth.models import User


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tg_id = models.IntegerField(unique=True)
    
    def __str__(self):
            return f"{self.user} ({self.tg_id})"
    class Meta:
        verbose_name = "профиль администратора"
        verbose_name_plural = "Профили администраторов"

class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    tg_id = models.IntegerField(unique=True)
    def __str__(self):
        return f"{self.name} ({self.tg_id})"

    class Meta:
        verbose_name = "профиль пользователя"
        verbose_name_plural = "Профили пользователей"
 
class Subscription(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    subscription_date = models.DateField(null=True, blank=True)
    year = models.CharField(max_length=4)
    month = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.user.name} ({self.subscription_date} - {self.month})"

    class Meta:
        verbose_name = "подписки"
        verbose_name_plural = "Подписки"

class File(models.Model):
    year = models.CharField(max_length=4)
    category = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "файл"
        verbose_name_plural = "Файлы"

        
class FileGoogle(models.Model):
    file = models.OneToOneField(
        File, on_delete=models.CASCADE, related_name='files_google')
    google_id = models.CharField(max_length=40)
    link = models.TextField()
    
    def __str__(self):
        return f"{self.file.title} ({self.link})"
    
    class Meta:
        verbose_name = "гугл файл"
        verbose_name_plural = "Гугл файлы"

class FileTg(models.Model):
    file = models.OneToOneField(
        File, on_delete=models.CASCADE, related_name='files_tg')
    tg_id = models.CharField(max_length=100)
    ext = models.CharField(max_length=40)
    
    def __str__(self):
        return f"{self.file.title} ({self.ext})"
    class Meta:
        verbose_name = "телеграм файл"
        verbose_name_plural = "Телеграм файлы"
