"""beatVideo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import include,url
from beats import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('software/', views.software, name='software'),
    path('thanks/', views.thanks, name='thanks'),
    path('', views.home, name='home'),
    path('plans/<int:pk>', views.plan, name='plan'),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/signup/', views.SignUp.as_view(), name='signup'),
    path('join/', views.join, name='join'),
    path('checkout/', views.checkout, name='checkout'),
    path('downloadFile/',views.downloadFile, name='downloadFile'),
    path('deleteFile/',views.deleteFile, name='deleteFile'),
    path('auth/settings/', views.settings, name='settings'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('email_change/', views.email_change, name='email_change'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('create/', views.create, name='create')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)