from django.contrib import admin
from django.urls import path
from principal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('populate/', views.populate, name='populate'),
    path('populate/complete/', views.populate_complete, name='populate'),
]
