from django.urls import path
from . import views
app_name = 'fikir'
from django.contrib.auth import views as auth_views
urlpatterns = [
     path('anasayfa/', views.IndexView, name='IndexView'),
     path('', views.IndexView, name='IndexView'),
     path('giris/',  views.LoginView.as_view(), name='LoginView'),
     path('uyeol/',  views.UserFormView.as_view(), name='SignupView'),     
     path('cikis/', auth_views.logout,  {'next_page': "fikir:IndexView"},  name='Logout'),
]