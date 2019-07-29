from django.urls import path
from . import views
app_name = 'fikir'
from django.contrib.auth import views as auth_views
urlpatterns = [
     path('', views.IndexView, name='IndexView'),
     path('anasayfa/', views.TimelineView, name='TimelineView'),
     path('giris/',  views.LoginView.as_view(), name='LoginView'),
     path('uyeol/',  views.UserFormView.as_view(), name='SignupView'),     
     path('profil/',  views.ProfileView, name='ProfileView'),     
     path('yenifikir/',  views.NewIdeaView.as_view(), name='NewIdeaView'),     
     path('detay/',  views.DetailView, name='DetailView'),     
     path('cikis/', auth_views.logout,  {'next_page': "fikir:IndexView"},  name='Logout'),
     path('begen/', views.likeAnIdea,  name='LikeAnIdea'),
     path('hesapayarlari/', views.ProfileSettingsView.as_view(), name='ProfileSettings'),
     path('paroladegistir/', views.change_password ,  name='ChangePassword'),
#      path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#         views.activate, name='activate'),
]