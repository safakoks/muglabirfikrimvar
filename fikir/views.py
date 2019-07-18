from django.shortcuts import render
from django.shortcuts import render, get_object_or_404,redirect,reverse
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm
from django.views.generic.base import View
from django.contrib.auth.forms import *
# Create your views here.

def IndexView(request):
    template_name = 'fikir/index.html'
    return render(request, template_name, {})

class LoginView(View):
    form_class = AuthenticationForm
    template_name = "fikir/login.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            control = AuthenticationForm(data=request.POST)
            if (control.is_valid()):
                user = authenticate(username=username, password=password)
                if user.is_active:
                    login(request, user)
                    return redirect('fikir:IndexView')
        return render(request, self.template_name, {'form': form})