from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Department(models.Model):
    DepartmentName = models.CharField(max_length=100)
    Description = models.CharField(max_length=250)
    def __str__(self):
        return self.DepartmentName

class IdeaType(models.Model):
    IdeaName = models.CharField(max_length=100)
    Icon = models.CharField(max_length=250)
    def __str__(self):
        return self.IdeaName    

class Status(models.Model):
    StatusName = models.CharField(max_length=100)
    StatusDescription = models.CharField(max_length=250)
    def __str__(self):
        return self.StatusName

class Adress(models.Model):
    District = models.CharField(max_length=100)
    Neighborhood = models.CharField(max_length=250)
    Street = models.CharField(max_length=100)
    AdressDesc = models.CharField(max_length=250)
    def __str__(self):
        return self.District

class Keyword(models.Model):
    Word = models.CharField(max_length=100)
    Idea= models.CharField(max_length=250)
    def __str__(self):
        return self.Word

class Photo(models.Model):
    Image = models.ImageField()
    def __str__(self):
        return self.Image


class Idea(models.Model):
    Title = models.CharField(primary_key=True,max_length=100)
    ideatype = models.ForeignKey(IdeaType,null=True,on_delete=models.PROTECT)
    Description = models.CharField(max_length=100)
    adress = models.ForeignKey(Adress,null=True,on_delete=models.PROTECT)
    department = models.ForeignKey(Department,on_delete=models.PROTECT)
    CreatedDate = models.DateTimeField(auto_now_add=True,blank=True)
    IgnoreDesc = models.CharField(max_length=500)
    IsApproved = models.BooleanField(default=True)
    IsActive = models.BooleanField(default=True)
    status = models.ForeignKey(Status,null=True,on_delete=models.PROTECT)
    def __str__(self):
        return self.Title

class UserProfile(models.Model):
    Name = models.CharField(max_length=100)
    Surname = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=100)
    Birthday = models.DateTimeField(auto_now_add=True,blank=True)
    Email = models.EmailField()
    ProfilePhoto =models.ImageField()
    UserT = models.OneToOneField(User,on_delete=models.CASCADE)

class UserLike(models.Model):
    User = models.ForeignKey(UserProfile,on_delete=models.PROTECT)
    Idea = models.ForeignKey(Idea,null=True,on_delete=models.PROTECT)
    LikeDate = models.DateTimeField(auto_now_add=True,blank=True)
    def __str__(self):
        return self.User







