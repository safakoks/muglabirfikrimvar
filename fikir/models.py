from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Department(models.Model):
    DepartmentName = models.CharField(max_length=100,verbose_name='Departman Adı')
    Description = models.CharField(max_length=250,verbose_name='Departman Açıklaması')
    class Meta:
        verbose_name = "Departman"
        verbose_name_plural = "Departmanlar"
    def __str__(self):
        return self.DepartmentName

class IdeaType(models.Model):
    IdeaName = models.CharField(max_length=100,verbose_name='Fikir Adı')
    Icon = models.CharField(max_length=250,verbose_name='Fikir Logosu')
    class Meta:
        verbose_name = "Fikir Tipi"
        verbose_name_plural = "Fikir Tipleri"
    def __str__(self):
        return self.IdeaName    

class Status(models.Model):
    StatusName = models.CharField(max_length=100,verbose_name='Fikir Durumu')
    StatusDescription = models.CharField(max_length=250,verbose_name='Fikir Durumu Açıklaması')
    class Meta:
        verbose_name = "Durum"
        verbose_name_plural = "Durumlar"
    def __str__(self):
        return self.StatusName

class Adress(models.Model):
    District = models.CharField(max_length=100,verbose_name='İlçe')
    Neighborhood = models.CharField(max_length=250,verbose_name='Semt')
    Street = models.CharField(max_length=100,verbose_name='Sokak')
    AdressDesc = models.CharField(max_length=250,verbose_name='Adres Açıklaması')
    class Meta:
        verbose_name = "Adres"
        verbose_name_plural = "Adresler"
    def __str__(self):
        return self.District

class Keyword(models.Model):
    Word = models.CharField(max_length=100,verbose_name='Anahtar Kelime')
    Idea= models.CharField(max_length=250,verbose_name='Fikir')
    class Meta:
        verbose_name = "Anahtar Kelime"
        verbose_name_plural = "Anahtar Kelimeler"
    def __str__(self):
        return self.Word

class Photo(models.Model):
    Image = models.ImageField(verbose_name='Fotoğraf')
    class Meta:
        verbose_name = "Fotoğraf"
        verbose_name_plural = "Fotoğraflar"
    def __str__(self):
        return self.Image


class Idea(models.Model):
    Title = models.CharField(primary_key=True,max_length=100,verbose_name='Başlık')
    ideatype = models.ForeignKey(IdeaType,null=True,on_delete=models.PROTECT,verbose_name='Fikir Tipi')
    Description = models.CharField(max_length=250,verbose_name='Açıklama')
    adress = models.ForeignKey(Adress,null=True,on_delete=models.PROTECT,verbose_name='Adres')
    department = models.ForeignKey(Department,on_delete=models.PROTECT,verbose_name='Departman')
    CreatedDate = models.DateTimeField(auto_now_add=True,blank=True,verbose_name='Yaratılış Tarihi')
    IgnoreDesc = models.CharField(max_length=500,verbose_name='Red Açıklaması')
    IsApproved = models.BooleanField(default=True,verbose_name='Onaylandı mı?')
    IsActive = models.BooleanField(default=True,verbose_name='Aktiflik Durumu')
    status = models.ForeignKey(Status,null=True,on_delete=models.PROTECT,verbose_name='Durum')
    class Meta:
        verbose_name = "Fikir"
        verbose_name_plural = "Fikirler"
    def __str__(self):
        return self.Title

class UserProfile(models.Model):
    Name = models.CharField(max_length=100,verbose_name='Ad')
    Surname = models.CharField(max_length=100,verbose_name='Soyad')
    PhoneNumber = models.CharField(max_length=100,verbose_name='Telefon Numarası')
    Birthday = models.DateTimeField(auto_now_add=True,blank=True,verbose_name='Doğum Tarihi')
    Email = models.EmailField(verbose_name='Email')
    ProfilePhoto =models.ImageField(verbose_name='Profil Fotoğrafı')
    UserT = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='Kullanıcı')
    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"
    def __str__(self):
        return self.Name + " " + self.Surname
  
class UserLike(models.Model):
    User = models.ForeignKey(UserProfile,on_delete=models.PROTECT,verbose_name='Kullanıcı')
    Idea = models.ForeignKey(Idea,null=True,on_delete=models.PROTECT,verbose_name='Fikir')
    LikeDate = models.DateTimeField(auto_now_add=True,blank=True,verbose_name='Beğenme Tarihi')
    class Meta:
        verbose_name = "Beğeni"
        verbose_name_plural = "Beğeniler"
    def __str__(self):
        return self.User







