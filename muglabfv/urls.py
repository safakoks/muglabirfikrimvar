"""muglabfv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from .api_router import router
from rest_framework.authtoken import views as api_auth_views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fikir.urls')),
    url(r'^parola_sifirla/$', auth_views.password_reset, name='password_reset'),
    url(r'^parola_sifirla/basarili/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^sifirla/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^sifirla/basarili/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # api
    path('api/', include(router.urls), name='api'),
    path('api-token-auth/', api_auth_views.obtain_auth_token, name='api_token_auth'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
