from django.shortcuts import render, redirect, get_object_or_404
from principal.models import Occupation, Genre, UserInformation, Film, Rating
from datetime import datetime
import os
from principal.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches
import shelve
from principal.forms import UserForm, FilmForm

def index(request):
    return render(request, "principal/base.html")

def cargar_datos(request):
    Rating.objects.all().delete()
    Film.objects.all().delete()
    UserInformation.objects.all().delete()
    Genre.objects.all().delete()
    Occupation.objects.all().delete()

    module_dir = os.path.dirname(__file__)
    with open(module_dir + "/data/ml-100k/u.occupation", "r", encoding="utf8", errors="ignore") as f:
        print("Cargando occupations...")
        lines = f.read().splitlines()
        occupations = []
        for line in lines:
            if line == "":
                continue
            occupation = line.split("|")
            occupations.append(Occupation(occupationName=occupation[0]))
        Occupation.objects.bulk_create(occupations)
        print("...occupations cargadas!")

    with open(module_dir + "/data/ml-100k/u.genre", "r", encoding="utf8", errors="ignore") as f:
        print("Cargando Genre...")
        lines = f.read().splitlines()
        genres = []
        for line in lines:
            if line == "":
                continue
            genre = line.split("|")
            genres.append(Genre(id=int(genre[1].strip()),genreName=genre[0]))
        Genre.objects.bulk_create(genres)
        print("...Genre cargadas!")

    with open(module_dir + "/data/ml-100k/u.item", "r", encoding="utf8", errors="ignore") as f:
        print("Cargando movies...")
        lines = f.read().splitlines()
        movies = []
        for line in lines:
            if line == "":
                continue
            movie = line.split("|")

            try:
                date_rel = datetime.strptime(movie[2].strip(),'%d-%b-%Y')
            except:
                date_rel = datetime.strptime('01-Jan-1990','%d-%b-%Y')

            try:
                date_rel_video = datetime.strptime(movie[3].strip(),'%d-%b-%Y')
            except:
                date_rel_video = date_rel

            movies.append(Film(id=int(movie[0].strip()) ,movieTitle=movie[1].strip(), releaseDate=date_rel, releaseVideoDate=date_rel_video, IMDbURL=movie[4].strip()))
        Film.objects.bulk_create(movies)
        print("...movies cargadas!")

    with open(module_dir + "/data/ml-100k/u.user", "r", encoding="utf8", errors="ignore") as f:
        print("Cargando Usuarios...")
        lines = f.read().splitlines()
        usuarios = []
        dict={}
        for line in lines:
            usuario = line.split("|")
            if len(usuario) != 5:
                continue
            id = int(usuario[0].strip())
            age = usuario[1]
            gender = usuario[2]
            zipCode = usuario[4].strip()
            usuarios.append(UserInformation(id=id, age=age, gender=gender, occupation=Occupation.objects.get(occupationName = usuario[3].strip()), zipCode=zipCode))
            dict[id] = usuarios
        UserInformation.objects.bulk_create(usuarios)
        print("...Usuarios cargadas!")

    with open(module_dir + "/data/ml-100k/u.data", "r", encoding="utf8", errors="ignore") as f:
        print("Cargando Rating...")
        lines = f.read().splitlines()
        ratings = []
        for line in lines:
            if line == "":
                continue
            rating = line.split("\t")
            ratings.append(Rating(user_id = int(rating[0].strip()), film_id = int(rating[1].strip()), rating=int(rating[2].strip()), rateDate= datetime.fromtimestamp(int(rating[3].strip())) ))
        Rating.objects.bulk_create(ratings)
        print("...Rating cargadas!")

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