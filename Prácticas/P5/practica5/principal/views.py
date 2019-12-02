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


def populate_municipios(request):
    PopulateDatabase.import_data('Municipio')
    last_action = 'Última acción realizada correctamente: ' + str(datetime.now())
    return render(request, 'populate.html', {'last_action_c': last_action, 'STATIC_URL': settings.STATIC_URL})


def populate_tipoeventos(request):
    PopulateDatabase.import_data('Tipo_JA')
    last_action = 'Última acción realizada correctamente: ' + str(datetime.now())
    return render(request, 'populate.html', {'last_action_o': last_action, 'STATIC_URL': settings.STATIC_URL})


def populate_lenguajes(request):
    PopulateDatabase.import_data('Lenguaje')
    last_action = 'Última acción realizada correctamente: ' + str(datetime.now())
    return render(request, 'populate.html', {'last_action_u': last_action, 'STATIC_URL': settings.STATIC_URL})


def populate_eventos(request):
    PopulateDatabase.import_data('Evento')
    last_action = 'Última acción realizada correctamente: ' + str(datetime.now())
    return render(request, 'populate.html', {'last_action_f': last_action, 'STATIC_URL': settings.STATIC_URL})