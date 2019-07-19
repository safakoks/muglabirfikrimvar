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
     path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]