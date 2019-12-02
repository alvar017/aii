from principal.models import Lenguaje
from principal.models import Municipio
from principal.models import Tipo_Evento
from principal.models import Evento
from datetime import datetime
from principal.progressbar import printProgressBar
import sys


def read_file(file_dir):
    res = []
#    with open('../data/ml-100k/' + file_dir) as f:
    with open('data/ml-100k/' + file_dir) as f:
        lines = f.read().splitlines()
        for line in lines:
            if ';' in line:
                aux = line.replace('\n', '').split(';')
                res.append(aux)
            else:
                line_aux = line.replace('\n', '').replace('\t', '').isdigit()
                if line_aux:
                    aux = line.split('\t')
                    res.append(aux)
                else:
                    res.append(line)
    return res


def import_lenguaje():
    print('Indexing lenguaje... look at progress:')
    Lenguaje.objects.all().delete()
    lenguajes = read_file('lenguas.csv')
    res = []
    z = 0
    for lenguaje in lenguajes:
        try:
            printProgressBar(z, len(lenguajes))
            if len(lenguaje) > 1:
                nombre = lenguaje[1]
                res.append(Lenguaje(nombre=nombre))
            z += 1
        except:
            e = sys.exc_info()[0]
            print("Error when creating a lenguaje: {0}".format(e))
            print('The value ' + str(lenguaje) + ' can not be index\n')
    Lenguaje.objects.bulk_create(res)
    print(str(len(res)) + ' lenguaje indexes\n')


def import_municipio():
    print('Indexing municipios... look at progress:')
    Municipio.objects.all().delete()
    municipios = read_file('municipio.csv')
    z = 0
    res = []
    for municipio in municipios:
        try:
            printProgressBar(z, len(municipios))
            municipio = str(municipio).strip()
            if municipio is not '':
                res.append(Municipio(nombre=str(municipio)))
            z += 1
        except:
            e = sys.exc_info()[0]
            print("Error when creating an municipio: {0}".format(e))
            print('The value ' + str(municipio) + ' can not be index\n')
    Municipio.objects.bulk_create(res)
    print(str(len(res)) + ' municipio indexes\n')

def import_tipoEventos():
    print('Indexing occupations... look at progress:')
    Tipo_Evento.objects.all().delete()
    tipoEventos = read_file('tipoevento.csv')
    z = 0
    res = []
    for tipoEvento in tipoEventos:
        try:
            printProgressBar(z, len(tipoEventos))
            tipoEvento = str(tipoEvento).strip()
            if tipoEvento is not '':
                res.append(Tipo_Evento(nombre=str(tipoEvento)))
            z += 1
        except:
            e = sys.exc_info()[0]
            print("Error when creating an tipo_evento: {0}".format(e))
            print('The value ' + str(tipoEvento) + ' can not be index\n')
    Tipo_Evento.objects.bulk_create(res)
    print(str(len(res)) + ' tipoEventos indexes\n')


def import_eventos():
    print('Indexing eventos... look at progress:')
    Evento.objects.all().delete()
    through_model = Evento.lenguajes.through
    eventos_lines = read_file('dataset-A.csv')
    eventos = []
    relations = []
    z = 0
    for evento in eventos_lines:
        try:
            printProgressBar(z, len(eventos_lines))
            nombre = evento[0].strip()
            tipo_evento = Tipo_Evento.objects.get(nombre=str(evento[1].strip())) 
            date = evento[2].strip()
            fecha_inicio_evento = None if len(date) == 0 else datetime.strptime(date, '%d/%m/%Y')
            nombre_lugar = evento[4]
            municipio = Municipio.objects.get(nombre=str(evento[5]))
            pais = evento[6].strip()

            eventos.append(Evento(nombre=nombre, tipo_evento=tipo_evento, fecha_inicio_evento=fecha_inicio_evento, nombre_lugar=nombre_lugar, municipio=municipio, pais=pais ))
            i = 3
            lenguajes_aux = []
            if "/" in evento[3]:
                lenguajes_aux = evento[3].split("/")
            else:
                lenguajes_aux.append(evento[3].strip())   
            
            j = 0
            while j < len(lenguajes_aux):
                lenguaje = Lenguaje.objects.get(nombre=lenguajes_aux[j])
                relations.append(through_model(lenguaje=lenguaje))
                j += 1
            z += 1
        except:
            e = sys.exc_info()[0]
            print("Error when creating a evento: {0}".format(e))
            print('The value ' + str(evento) + ' can not be index\n')
    Evento.objects.bulk_create(eventos)
    through_model.objects.bulk_create(relations)
    print(str(z) + ' eventos indexes\n')


def import_data(selection):
    i = 0
    if 'Lenguaje' in selection:
        import_lenguaje()
        i += 1
    if 'Municipio' in selection:
        import_municipio()
        i += 1
    if 'Tipo_Evento' in selection:
        import_tipoEventos()
        i += 1
    if 'Evento' in selection:
        import_eventos()
        i += 1
    if 'all' in selection:
        import_lenguaje()
        import_municipio()
        import_tipoEventos()
        import_eventos()
        i += 4
    if i == 0:
        print('Nothing to import! Use a string array with your selection\n')
        print('It can be categories, occupations, users, film or punctuations\n')
        print("Example: ['categories', 'occupations'])")
        print("Use ['all'] for a complete indexation)")


#if __name__ == '__main__':
#    import_data('all')