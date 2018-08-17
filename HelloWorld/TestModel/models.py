from django.db import models

# Create your models here.
from django.db import models
class Test(models.Model):
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=10,default='888888')