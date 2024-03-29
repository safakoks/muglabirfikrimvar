from django.urls import path
from . import views, ajax_view
app_name = 'fikir'
from django.contrib.auth import views as auth_views
urlpatterns = [
     path('', views.IndexView, name='IndexView'),
     path('anasayfa/', views.TimelineView, name='TimelineView'),
     path('giris/',  views.LoginView.as_view(), name='LoginView'),
     path('uyeol/',  views.UserFormView.as_view(), name='SignupView'),     
     path('yenifikir/',  views.NewIdeaView.as_view(), name='NewIdeaView'),  

     path('fikirguncelle/<int:pk>',  views.UpdateIdeaView.as_view(), name='UpdateIdeaView'),
     path('sil/<int:pk>',  views.IdeaDelete, name='DeleteIdea'),




     path('detay/<int:pk>',  views.DetailView, name='DetailView'),     
     path('cikis/', auth_views.logout,  {'next_page': "fikir:IndexView"},  name='Logout'),
     path('hesapayarlari/', views.ProfileSettingsView.as_view(), name='ProfileSettings'),
     path('paroladegistir/', views.change_password ,  name='ChangePassword'),

     # profile listeleme
     path('profil/',  views.ProfileView, name='ProfileView'),     
     path('profil/begendigim',  views.MyLikeProfileView, name='MyLikeProfileView'),     



     # anasayfa filtreleme
     path('anasayfa/haftanınenleri',  views.best_of_week, name='best_of_week_view'),     
     path('anasayfa/ayinenleri',  views.best_of_month, name='best_of_month_view'),     
     path('anasayfa/gerceklestirilenler',  views.done_ideas, name='done_ideas_view'),     
     path('anasayfa/zamanagore-ilk',  views.ideas_by_time, name='ideas_by_time_view'),     
     path('anasayfa/zamanagore-son',  views.ideas_by_desc_time, name='ideas_by_desc_time_view'),     
     path('anasayfa/eniyiler',  views.best_ideas, name='best_ideas_view'),  
     path('anasayfa/fikir-tipi/<int:pk>',  views.ideas_by_type, name='ideas_by_type_view'),  

     
     # arama   
     path('anasayfa/arama',  views.search_idea, name='search_idea_view'),     

     # ajax
     path('ajax/load-neighborhoods/', ajax_view.load_neighborhood, name='ajax_load_neighborhoods'),
     path('ajax/load-streets/', ajax_view.load_street, name='ajax_load_streets'),
     path('begen/', ajax_view.likeAnIdea,  name='LikeAnIdea'),


#      path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#         views.activate, name='activate'),
]