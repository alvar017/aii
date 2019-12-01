from django.db.models import Count, Avg
from django.shortcuts import render
from django.conf import settings
from principal import PopulateDatabase
from principal import forms
from principal.models import *
from datetime import *


def index(request):
    return render(request, 'index.html',)


def populate(request):
    return render(request, 'populate.html',)


def populate_complete(request):
    PopulateDatabase.import_data('all')
    last_action = 'Última acción realizada correctamente: ' + str(datetime.now())
    return render(request, 'populate.html', {'last_action_a': last_action, 'STATIC_URL': settings.STATIC_URL})


def populate_categories(request):
    PopulateDatabase.import_data('categories')
    last_action = 'Última acción realizada correctamente: ' + str(datetime.now())
    return render(request, 'populate.html', {'last_action_c': last_action, 'STATIC_URL': settings.STATIC_URL})


def populate_occupations(request):
    PopulateDatabase.import_data('occupations')
    last_action = 'Última acción realizada correctamente: ' + str(datetime.now())
    return render(request, 'populate.html', {'last_action_o': last_action, 'STATIC_URL': settings.STATIC_URL})


def populate_users(request):
    PopulateDatabase.import_data('users')
    last_action = 'Última acción realizada correctamente: ' + str(datetime.now())
    return render(request, 'populate.html', {'last_action_u': last_action, 'STATIC_URL': settings.STATIC_URL})


def populate_films(request):
    PopulateDatabase.import_data('films')
    last_action = 'Última acción realizada correctamente: ' + str(datetime.now())
    return render(request, 'populate.html', {'last_action_f': last_action, 'STATIC_URL': settings.STATIC_URL})


def populate_punctuations(request):
    PopulateDatabase.import_data('punctuations')
    last_action = 'Última acción realizada correctamente: ' + str(datetime.now())
    return render(request, 'populate.html', {'last_action_p': last_action, 'STATIC_URL': settings.STATIC_URL})


def users(request):
    users_query = User.objects.all().order_by('occupation')
    return render(request, 'users.html', {'users_query': users_query, 'STATIC_URL': settings.STATIC_URL})


def best_films(request):
    films_query = Film.objects.annotate(avg_p=Avg('punctuation__rank')).order_by('-avg_p')[:5]
    return render(request, 'best_films.html', {'films_query': films_query, 'STATIC_URL': settings.STATIC_URL})


def search_films(request):
    form = forms.FilmSearchByYearForm()
    films = None

    if request.method == 'POST':
        form = forms.FilmSearchByYearForm(request.POST)

        if form.is_valid():
            films = Film.objects.filter(release_date__year=form.cleaned_data['year'])

    return render(request, 'search_films.html',
                  {'formulario': form, 'peliculas': films, 'STATIC_URL': settings.STATIC_URL})


def search_punctuation(request):
    return render(request, 'search_punctuations.html',)
