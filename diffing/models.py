from django.db import models

# Create your models here.


class Job(models.Model):
    metric = models.SlugField()