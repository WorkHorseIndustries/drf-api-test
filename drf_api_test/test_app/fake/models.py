from django.db import models

# Create your models here.
class Fake(models.Model):

    name = models.CharField(max_length=10)
