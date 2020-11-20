from django.db import models

# Create your models here.


class Job(models.Model):
    metric = models.SlugField()
    ready = models.BooleanField(default=False)
    file_name = models.CharField(max_length=100, blank=True)
