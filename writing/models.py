from django.db import models
from accounts.models import User

class Sentence(models.Model):
    sentence = models.CharField(max_length=200)
    discription = models.CharField(max_length=200)
    created_at = models.DateTimeField(null=True)
    translate = models.CharField(max_length=200, null=True)
    korean = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.discription

class Post(models.Model):
    body = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, null=True)
    like_users = models.ManyToManyField(User, related_name='like', null=True)
    like_num = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    unknown = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.body
    
class Subsription(models.Model):
    sub_email = models.EmailField(unique=True, max_length=50)
    sub_nickname = models.CharField(max_length=50, unique=True, null=True)