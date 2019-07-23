from django.contrib.auth.models import User
from .models import UserProfile, Idea,IdeaType,Address,Department
from django import  forms
from captcha.fields import ReCaptchaField
import datetime



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


class NewIdeaForm(forms.ModelForm):
    title           = forms.CharField(
        max_length=100,
        label='Fikir Başlığı',
        help_text='Fikir başlığı en fazla 100 karakter içerebilir',
        error_messages={'required': 'Lütfen fikir başlığı giriniz'})
    ideatype = forms.ModelChoiceField(queryset=IdeaType.objects.all(),
        label='Fikir Tipi',
        help_text='Fikir tipi en fazla 100 karakter içerebilir')
    department =forms.ModelChoiceField(queryset=Department.objects.all(),
        label='Bölüm',
        help_text='Lütfen birini seçiniz',)
    description     = forms.CharField(widget=forms.Textarea,
        max_length=300,
        label='Açıklama',
        help_text='En fazla 300 karekter girebilirsiniz')
    district        = forms.CharField(
        max_length=50,
        label='İlçe ',
        help_text='En fazla 50 karekter içerir')
    neighborhood    = forms.CharField(
        max_length=50,
        label='Mahalle',
        help_text='En fazla 50 karekter içerir')
    street  = forms.CharField(
        max_length=50,
        label='Cadde',
        help_text='En fazla 50 karekter içerir')
    adressDesc      = forms.CharField(widget=forms.Textarea,
        max_length=200,
        label='Adres',
        help_text='En fazla 200 karekter girebilirsiniz')
 
    ideaPhoto1      = forms.ImageField(label='Fikir Fotoğrafı 1')
    ideaPhoto2      = forms.ImageField(label='Fikir Fotoğrafı 2')
    ideaPhoto3      = forms.ImageField(label='Fikir Fotoğrafı 3')
      
         
    class Meta:
        model = Idea
        fields = [
            'title',
            'ideatype',
            'department',
            'description',
            'district',
            'neighborhood',
            'street',
            'adressDesc',
            'ideaPhoto1',
            'ideaPhoto2',
            'ideaPhoto3']

    def __init__(self, *args, **kwargs):
        super(NewIdeaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.request = kwargs.pop('request', None)
        # companyid = self.request.user.get_profile().main_contactnum.clientid.idflcustomernum
        # self.fields['adress'].queryset = Adress.objects.filter(clientid__exact=companyid)
       