from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("load_data/", views.cargar_datos),
    path("loadRS/", views.loadRS),
    path("search/", views.search),
    path("recommendedFilmsItems/", views.recommendedFilmsItems),
    path("recommendedFilmsUser/", views.recommendedFilmsUser),
    path("recommendedUsersFilms/", views.recommendedUsersFilms),
    path("similarFilms/", views.similarFilms)
]
