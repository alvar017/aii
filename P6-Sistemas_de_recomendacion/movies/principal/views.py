from django.shortcuts import render, redirect, get_object_or_404
from principal.models import Puntuacion, Libro
from datetime import datetime
import os
from principal.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches
import shelve
from principal.forms import UserForm, FilmForm

def index(request):
    return render(request, "principal/base.html")

def cargar_datos(request):
    Puntuacion.objects.all().delete()
    Libro.objects.all().delete()
    
    module_dir = os.path.dirname(__file__)
    with open(module_dir + "/data/ml-100k/bookfeatures.csv", "r", encoding="utf8") as f:
        print("Cargando libros...")
        lines = f.read().splitlines()
        libros = []
        for line in lines:
            if line == "":
                continue
            libro = line.split(";")
            book_id  = libro[0]
            titulo = libro[1]
            autor = libro[2]
            genero = libro[3]
            idioma = libro[4]
            rating1 = libro[5]
            rating2 = libro[6]
            rating3 = libro[7]
            rating4 = libro[8]
            rating5 = libro[9]
            print(libro)
            libros.append(Libro(book_id=book_id, titulo=titulo, autor=autor, genero=genero, idioma=idioma, rating1=rating1, rating2=rating2, rating3=rating3, rating4=rating4, rating5=rating5))
        Libro.objects.bulk_create(libros)
        print("...libros cargados!")

    with open(module_dir + "/data/ml-100k/ratings.csv", "r", encoding="utf8", errors="ignore") as f:
        print("Cargando puntuaciones...")
        lines = f.read().splitlines()
        puntuaciones = []
        for line in lines[1:]:
            if line == "":
                continue
            puntuacion = line.split(";")
            value = puntuacion[0]
            usuario_id = puntuacion[1]
            book_id = puntuacion[2]
            puntuaciones.append(Puntuacion(value=value, usuario_id=usuario_id, book_id=book_id))
        Puntuacion.objects.bulk_create(puntuaciones)
        print("...puntuaciones cargadas!")

    return render(request, "principal/load_data_success.html")

# Funcion que carga en el diccionario Prefs todas las puntuaciones de usuarios a peliculas. 
# Tambien carga el diccionario inverso y la matriz de similitud entre items
# Serializa los resultados en dataRS.dat
def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Rating.objects.all()
    for ra in ratings:
        user = int(ra.user.id)
        itemid = int(ra.film.id)
        rating = float(ra.rating)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()

def loadRS(request):
    loadDict()
    return render(request,'principal/loadRS.html')

#APARTADO A
def search(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(UserInformation, pk=idUser)
            return render(request,'principal/ratedFilms.html', {'usuario':user})
    form=UserForm()
    return render(request,'principal/search_user.html', {'form':form })

# APARTADO B
def recommendedFilmsItems(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(UserInformation, pk=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()
            rankings = getRecommendedItems(Prefs, SimItems, int(idUser))
            recommended = rankings[:2]
            films = []
            scores = []
            for re in recommended:
                films.append(Film.objects.get(pk=re[1]))
                scores.append(re[0])
            items= zip(films,scores)
            return render(request,'principal/recommendationItems.html', {'user': user, 'items': items})
    form = UserForm()
    return render(request,'principal/search_user.html', {'form': form})

# APARTADO C
def recommendedFilmsUser(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(UserInformation, pk=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            shelf.close()
            rankings = getRecommendations(Prefs,int(idUser))
            recommended = rankings[:2]
            films = []
            scores = []
            for re in recommended:
                films.append(Film.objects.get(pk=re[1]))
                scores.append(re[0])
            items= zip(films,scores)
            return render(request,'principal/recommendationItems.html', {'user': user, 'items': items})
    form = UserForm()
    return render(request,'principal/search_user.html', {'form': form})

# APARTADO D
def recommendedUsersFilms(request):
    if request.method=='GET':
        form = FilmForm(request.GET, request.FILES)
        if form.is_valid():
            idFilm = form.cleaned_data['id']
            film = get_object_or_404(Film, pk=idFilm)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['ItemsPrefs']
            shelf.close()
            rankings = getRecommendations(Prefs,int(idFilm))
            recommended = rankings[:3]
            films = []
            scores = []
            for re in recommended:
                films.append(UserInformation.objects.get(pk=re[1]))
                scores.append(re[0])
            items= zip(films,scores)
            return render(request,'principal/recommendationUsers.html', {'film': film, 'items': items})
    form = FilmForm()
    return render(request,'principal/search_film.html', {'form': form})

# APARTADO E
def similarFilms(request):
    film = None
    if request.method=='GET':
        form = FilmForm(request.GET, request.FILES)
        if form.is_valid():
            idFilm = form.cleaned_data['id']
            film = get_object_or_404(Film, pk=idFilm)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, int(idFilm),n=3)
            films = []
            similar = []
            for re in recommended:
                films.append(Film.objects.get(pk=re[1]))
                similar.append(re[0])
            items= zip(films,similar)
            return render(request,'principal/similarFilms.html', {'film': film,'films': items})
    form = FilmForm()
    return render(request,'principal/search_film.html', {'form': form})