from django.urls import path
from . import views
app_name = 'fikir'
from django.contrib.auth import views as auth_views
urlpatterns = [
     path('anasayfa/', views.IndexView, name='IndexView'),
     path('giris/',  auth_views.login, {'template_name': 'fikir/login.html'}, name='LoginView'),
     path('cikis/', auth_views.logout,  {'next_page': "fikir:IndexView"},  name='Logout'),
]