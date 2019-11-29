from django.shortcuts import render, redirect
from principal.models import Pelicula, Categoria, Ocupacion, Usuario, Puntuacion
import datetime
from django.db.models import Avg
import os
from .forms import YearForm, UserForm, CatForm

def index(request):
    return render(request, "principal/base.html")

def cargar_datos(request):
    Ocupacion.objects.all().delete()
    Categoria.objects.all().delete()
    Usuario.objects.all().delete()
    Pelicula.objects.all().delete()
    Puntuacion.objects.all().delete()
    module_dir = os.path.dirname(__file__)

    # Categorías
    with open(
        module_dir + "/data/ml-100k/u.genre", "r", encoding="utf8", errors="ignore"
    ) as f:
        print("Cargando categorías...")
        lines = f.read().splitlines()
        categorias = []
        for line in lines:
            if line == "":
                continue
            categoria = line.split("|")
            id_categoria = int(categoria[1])
            nombre = categoria[0]
            categorias.append(Categoria(id_categoria=id_categoria, nombre=nombre,))
        Categoria.objects.bulk_create(categorias)
        print("...categorías cargadas!")

    # Películas
    with open(
        module_dir + "/data/ml-100k/u.item", "r", encoding="utf8", errors="ignore"
    ) as f:
        print("Cargando películas...")
        lines = f.read().splitlines()                
        ThroughModel = Pelicula.categorias.through        
        peliculas = []
        relations = []
        for line in lines:
            if line == "":
                continue
            pelicula = line.split("|")
            id_pelicula = int(pelicula[0])
            titulo = pelicula[1]
            fecha_estreno = pelicula[2]
            if fecha_estreno == "":
                fecha_estreno_obj = None
            else:
                fecha_estreno_obj = datetime.datetime.strptime(
                    fecha_estreno, "%d-%b-%Y"
                ).date()
            url = pelicula[3]
            peliculas.append(Pelicula(id_pelicula=id_pelicula, titulo=titulo, fecha_estreno=fecha_estreno_obj, url=url,))
            #Categorías
            for i in range(5, 20):
                cat_id = i - 5
                if pelicula[i] == "1":
                    cat = Categoria.objects.get(id_categoria=cat_id)
                    relations.append(ThroughModel(categoria=cat, pelicula_id=id_pelicula))

        Pelicula.objects.bulk_create(peliculas)
        ThroughModel.objects.bulk_create(relations)
        print("...películas cargadas!")

    # Ocupaciones
    with open(
        module_dir + "/data/ml-100k/u.occupation", "r", encoding="utf8", errors="ignore"
    ) as f:
        print("Cargando ocupaciones...")
        lines = f.read().splitlines()
        ocupaciones = []
        for line in lines:
            if line == "":
                continue
            nombre = line
            ocupaciones.append(Ocupacion(nombre=nombre))
        Ocupacion.objects.bulk_create(ocupaciones)
        print("...ocupaciones cargadas!")

    # Usuarios
    with open(
        module_dir + "/data/ml-100k/u.user", "r", encoding="utf8", errors="ignore"
    ) as f:
        print("Cargando usuarios...")
        lines = f.read().splitlines()
        usuarios = []
        for line in lines:
            if line == "":
                continue
            usuario = line.split("|")
            id_usuario = int(usuario[0])
            edad = int(usuario[1])
            sexo = usuario[2]
            ocupacion = Ocupacion.objects.get(nombre=usuario[3])
            codigo_postal = usuario[4]
            usuarios.append(Usuario(id_usuario=id_usuario,edad=edad,sexo=sexo,ocupacion=ocupacion,codigo_postal=codigo_postal,))
        Usuario.objects.bulk_create(usuarios)
        print("...usuarios cargados!")

    # Puntuacion
    with open(
        module_dir + "/data/ml-100k/u.data", "r", encoding="utf8", errors="ignore"
    ) as f:
        print("Cargando puntuaciones...")
        lines = f.read().splitlines()
        puntuaciones = []
        for line in lines:
            if line == "":
                continue
            puntuacion = line.split("\t")
            valoracion = puntuacion[2]
            puntuaciones.append(
                Puntuacion(valoracion=int(valoracion),usuario_id=puntuacion[0],pelicula_id=puntuacion[1])
            )
        Puntuacion.objects.bulk_create(puntuaciones)
        print("...puntuaciones cargadas!")

    return render(request, "principal/load_data_success.html")

def show_users_by_ocupacion(request):
    occupations = Ocupacion.objects.all()
    return render(
        request, "principal/user_list_occupation.html", {"occupations": occupations}
    )

def top5_peliculas(request):
    peliculas = Pelicula.objects.annotate(avg_rating=Avg("puntuacion__valoracion")).order_by("-avg_rating")[:5]
    return render(
        request, "principal/list_best_rated_films.html", {"peliculas": peliculas}
    )

def buscar_peliculas_by_year(request):
    if request.method == "POST":
        form = YearForm(request.POST)
        if form.is_valid():
            films = Pelicula.objects.filter(fecha_estreno__year=request.POST["year"])
            return render(
                request,
                "principal/search_film_by_year.html",
                {"form": form, "films": films},
            )
    else:
        form = YearForm()

    return render(request, "principal/search_film_by_year.html", {"form": form})

def buscar_puntuacion_usuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            ratings = Puntuacion.objects.filter(usuario_id=request.POST["user_id"])
            return render(
                request,
                "principal/search_user_ratings.html",
                {"form": form, "ratings": ratings},
            )
    else:
        form = UserForm()

    return render(request, "principal/search_user_ratings.html", {"form": form})

def buscar_peliculas_categoria(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        cat = CatForm(request.POST)
        print(cat)
        selected_value = request.POST['cat']
        print("AAAAAAAAAAAAAAAAAAA")
        print(selected_value)
        films = Pelicula.objects.filter(categorias__nombre__contains = selected_value)
        print(films)
        return render(
                request,
                "principal/add_spin_box_categoria.html",
                {"films": films, "categorias": categorias},
            )
    else:
        form = YearForm()
        return render(
                request,"principal/add_spin_box_categoria.html",{"categorias": categorias})