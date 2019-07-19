from django.contrib.auth.models import User
from .models import UserProfile
from django import  forms
import datetime



class LoginForm(forms.Form):
    username    = forms.CharField(max_length=50,label='Kullanıcı Adı')
    password    = forms.CharField(widget=forms.PasswordInput,label='Parola')
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    name        = forms.CharField(max_length=100,label='Ad')
    surname     = forms.CharField(max_length=100,label='Soyad')
    phoneNumber = forms.CharField(max_length=100,label='Telefon Numarası')
    birthday    = forms.DateField(label="Doğum Günü",initial=datetime.date.today)
    email       = forms.EmailField(label='Email')
    profilePhoto=forms.ImageField(label='Profil Fotoğrafı')
    username    = forms.CharField(max_length=50,label='Kullanıcı Adı')
    password    = forms.CharField(widget=forms.PasswordInput,label='Parola')
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['username', 'password', 'name','surname','phoneNumber','birthday','email','profilePhoto']