from django.db import models

# Create your models here.


class Pet(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=20, default="Not informed")
