from django.shortcuts import render
from principal import PopulateDatabase


def index(request):
    return render(request, 'index.html',)


def populate(request):
    return render(request, 'populate.html',)


def populate_complete(request):
    PopulateDatabase.import_data('all')
    return render(request, 'populate.html',)
