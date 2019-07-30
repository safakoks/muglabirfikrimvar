from django.contrib.auth.models import User
from .models import UserProfile, Idea,IdeaType,Department
from django import  forms
from captcha.fields import ReCaptchaField
import datetime
from django.contrib.auth.forms import PasswordChangeForm


class LoginForm(forms.Form):
    username    = forms.CharField(max_length=50,label='Kullanıcı Adı')
    password    = forms.CharField(widget=forms.PasswordInput,label='Parola')
    remember_me = forms.BooleanField(required=False,label='Beni Hatırla', widget=forms.CheckboxInput())


    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    name        = forms.CharField(max_length=100,label='Ad',help_text='Lütfen adınızı giriniz')
    surname     = forms.CharField(max_length=100,label='Soyad',help_text='Lütfen soyadınızı giriniz')
    phoneNumber = forms.CharField(max_length=100,label='Telefon Numarası')
    birthday    = forms.DateField(label="Doğum Günü",initial=datetime.date.today)
    email       = forms.EmailField(label='Email',help_text='*gerekli')
    profilePhoto= forms.ImageField(label='Profil Fotoğrafı',help_text='Lütfen profil fotoğrafınızı giriniz')
    username    = forms.CharField(max_length=50,label='Kullanıcı Adı')
    password    = forms.CharField(widget=forms.PasswordInput,label='Parola',help_text='*gerekli')
    captcha      = ReCaptchaField(label='')

    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['username', 'password', 'name','surname','phoneNumber','birthday','email','profilePhoto']


class UserEditForm(forms.ModelForm):
    Name        = forms.CharField(max_length=100,label='Ad',help_text='Lütfen adınızı giriniz')
    Surname     = forms.CharField(max_length=100,label='Soyad',help_text='Lütfen soyadınızı giriniz')
    PhoneNumber = forms.CharField(max_length=100,label='Telefon Numarası')
    Birthday    = forms.DateField(label="Doğum Günü",initial=datetime.date.today)
    Email       = forms.EmailField(label='Email',help_text='*gerekli')
    ProfilePhoto= forms.ImageField(label='Profil Fotoğrafı',help_text='Lütfen profil fotoğrafınızı giriniz')
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['ProfilePhoto'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = UserProfile
        fields = ['Name', 'Surname','PhoneNumber','Birthday','Email','ProfilePhoto']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=("Eski Parola"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': False}),
    )
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class NewIdeaForm(forms.ModelForm):
    Title           = forms.CharField(
        max_length=100,
        label='Fikir Başlığı',
        help_text='Fikir başlığı en fazla 100 karakter içerebilir',
        error_messages={'required': 'Lütfen fikir başlığı giriniz'})
    Ideatype = forms.ModelChoiceField(queryset=IdeaType.objects.all(),
        label='Fikir Tipi',
        help_text='Fikir tipi en fazla 100 karakter içerebilir')
    Department =forms.ModelChoiceField(queryset=Department.objects.all(),
        label='Bölüm',
        help_text='Lütfen birini seçiniz',)
    Description     = forms.CharField(widget=forms.Textarea,
        max_length=500,
        label='Açıklama',
        help_text='En fazla 500 karekter girebilirsiniz')
    District        = forms.CharField(
        max_length=50,
        label='İlçe ',
        help_text='En fazla 50 karekter içerir')
    Neighborhood    = forms.CharField(
        max_length=50,
        label='Mahalle',
        help_text='En fazla 50 karekter içerir')
    Street  = forms.CharField(
        max_length=50,
        label='Cadde',
        help_text='En fazla 50 karekter içerir')
    AdressDesc      = forms.CharField(widget=forms.Textarea,
        max_length=200,
        label='Adres Açıklaması',
        help_text='En fazla 200 karekter girebilirsiniz')
    ideaPhoto      = forms.ImageField(label='Fikrinizin Görseli')
      
    class Meta:
        model = Idea
        fields = [
            'Title',
            'Ideatype',
            'Department',
            'Description',
            'District',
            'Neighborhood',
            'Street',
            'AdressDesc',
            'ideaPhoto',
         ]

    def __init__(self, *args, **kwargs):
        super(NewIdeaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.request = kwargs.pop('request', None)
        # companyid = self.request.user.get_profile().main_contactnum.clientid.idflcustomernum
        # self.fields['adress'].queryset = Adress.objects.filter(clientid__exact=companyid)
 