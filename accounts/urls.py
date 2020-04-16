from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from .views import signup,signin,reset,verify
urlpatterns = [
    path('sign-up/',signup, name='sign-up'),
    path('sign-in/',signin, name='sign-in'),
    path('reset-password/',reset, name='reset'),
    path('verification/',verify, name='verify'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
