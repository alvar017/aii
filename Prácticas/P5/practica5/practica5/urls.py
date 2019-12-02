from django.contrib import admin
from django.urls import path
from principal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('populate/', views.populate, name='populate'),
    path('populate/complete/', views.populate_complete, name='populate'),
    path('populate/municipios/', views.populate_municipios, name='populate'),
    path('populate/tipoeventos/', views.populate_tipoeventos, name='populate'),
    path('populate/lenguajes/', views.populate_lenguajes, name='populate'),
    path('populate/eventos/', views.populate_eventos, name='populate'),
   
]
