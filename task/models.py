from django.db import models
from django.contrib.auth.models import User



# created your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    dateCompleted = models.DateTimeField(blank=True, null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        #return self.title + ' ' + self.user.username
        return f"ID: {self.user.id}, Título: {self.title}"