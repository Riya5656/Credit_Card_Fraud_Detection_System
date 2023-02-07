from django.contrib import admin
from django.urls import path,re_path
#from .views import home,predict,pred
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('form.html/', views.enter, name='form'),
    path('predict/', views.predict, name='predict'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact')
]