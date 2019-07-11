from django.db import models
from django.conf import settings

# Create your models here.
class Department(models.Model):
    DepartmentName = models.CharField(max_length=100)
    Description = models.CharField(max_length=250)


    def __str__(self):
        return self.DepartmentName