from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username
class Task(models.Model):
    task_name = models.CharField(max_length=255, null=True, blank=True)
    completed = models.BooleanField(default=False, null=True, blank=True)
    
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='owned_tasks', null=True, blank=True)
    payer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='paid_tasks', null=True, blank=True)

    def __str__(self):
        return self.task_name or "Unnamed Task"
class Contact(models.Model):
    name=models.CharField(max_length=50,null=False,blank=False)
    email=models.EmailField(null=True,blank=True)
    message=models.CharField(max_length=500,blank=False,null=False)