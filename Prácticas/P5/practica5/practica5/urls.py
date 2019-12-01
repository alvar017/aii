from django.contrib import admin
from django.urls import path
from principal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('populate/', views.populate, name='populate'),
    path('populate/complete/', views.populate_complete, name='populate'),
    path('populate/categories/', views.populate_categories, name='populate'),
    path('populate/occupations/', views.populate_occupations, name='populate'),
    path('populate/users/', views.populate_users, name='populate'),
    path('populate/films/', views.populate_films, name='populate'),
    path('populate/punctuations/', views.populate_punctuations, name='populate'),
    path('users/', views.users, name='users'),
    path('best_films/', views.best_films, name='best_films'),
    path('search_films/', views.search_films, name='search_films'),
    path('search_punctuations/', views.search_punctuation, name='search_punctuation'),
    path('search_category/', views.search_category, name='search_category'),
]
