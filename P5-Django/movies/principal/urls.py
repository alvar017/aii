from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("load_data/", views.cargar_datos),
    path("user_list_occupation/", views.show_users_by_ocupacion),
    path("list_best_rated_films/", views.top5_peliculas),
    path("search_film_by_year/", views.buscar_peliculas_by_year),
    path("search_user_ratings/", views.buscar_puntuacion_usuario),
    path("add_spin_box_categoria/", views.buscar_peliculas_categoria),
]
