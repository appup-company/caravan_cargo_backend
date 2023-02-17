from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils import timezone
import random


    
class User(AbstractUser):
    password = models.CharField(max_length=800, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']
    registered = models.BooleanField(default=False)

    # Address for delivery
    city = models.CharField(verbose_name='Город', max_length=100, null=True, blank=True)

    #push
    player_id = models.CharField(max_length=900, null=True, blank=True)


class Package(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='package_user')
    track_code = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='added')
    #Добавлено - added
    #Отправлено - sent
    #Прибыло - arrived
    #Выдано - given

    created_at = models.DateTimeField(default=timezone.now)
    weight = models.FloatField(max_length=50, null=True, blank=True)
    amount_income = models.FloatField(null=True, blank=True)


class Notification(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=220, null=True, blank=True)
    disappears = models.BooleanField(default=True)


class UserShowedNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='showed_user')
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='showed_notification')