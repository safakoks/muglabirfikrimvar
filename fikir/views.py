from django.shortcuts import render
from django.shortcuts import render, get_object_or_404,redirect,reverse
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.views.generic.base import View
from django.contrib.auth.forms import *
from .models import *
# Create your views here.

def IndexView(request):
    template_name = 'fikir/index.html'
    return render(request, template_name, {})

class LoginView(View):
    form_class = LoginForm
    template_name = "fikir/login.html"
    formVariables = {
    'form': form_class,
    'pagetitle':'Giriş',
    'formtitle':'Giriş',
    'buttontext' : 'Giriş',
    'warningmessage':''}
    def get(self, request):
        return render(request, self.template_name, self.formVariables)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('fikir:IndexView')
        self.formVariables["warningmessage"] = form.errors
        return render(request, self.template_name, self.formVariables)

class UserFormView(View):
    form_class = UserForm
    template_name = "fikir/login.html"
    formVariables = {'form': form_class(None),
    'pagetitle':'Üye Ol',
    'formtitle':'Üye Ol',
    'buttontext' : "Üye Ol",
    'warningmessage':''}
    def get(self, request):
            return render(request, self.template_name,self.formVariables)

    def post(self, request):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # Kullanici oluşturma
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            # Kullanıcıya bağlı kullanıcı profili oluşturma
            userprofile = UserProfile()
            userprofile.Name            = form.cleaned_data['name']
            userprofile.Surname         = form.cleaned_data['surname']
            userprofile.PhoneNumber     = form.cleaned_data['phoneNumber']
            userprofile.Birthday        = form.cleaned_data['birthday']
            userprofile.Email           = form.cleaned_data['email']
            userprofile.ProfilePhoto    = form.cleaned_data['profilePhoto']
            userprofile.UserT           = user
            userprofile.save()

            # Oluşturulan Kullanıcıyla giriş yapma
            user = authenticate(username = username,password= password)
            if  user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('fikir:IndexView')

        self.formVariables["warningmessage"] =form.errors
        return render(request,self.template_name,self.formVariables)
