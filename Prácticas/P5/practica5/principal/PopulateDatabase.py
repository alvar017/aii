from principal.models import Category
from principal.models import Occupation
from principal.models import User
from principal.models import Film
from principal.models import Punctuation
from datetime import datetime
from principal.progressbar import printProgressBar
import sys


def read_file(file_dir):
    res = []
#    with open('../data/ml-100k/' + file_dir) as f:
    with open('data/ml-100k/' + file_dir) as f:
        lines = f.read().splitlines()
        for line in lines:
            if '|' in line:
                aux = line.replace('\n', '').split('|')
                res.append(aux)
            else:
                line_aux = line.replace('\n', '').replace('\t', '').isdigit()
                if line_aux:
                    aux = line.split('\t')
                    res.append(aux)
                else:
                    res.append(line)
    return res


def import_categories():
    print('Indexing categories, show the progress:')
    Category.objects.all().delete()
    categories = read_file('u.genre')
    res = []
    z = 0
    for category in categories:
        try:
            printProgressBar(z, len(categories))
            if len(category) > 1:
                id_object = int(category[1])
                name_category = category[0]
                res.append(Category(category_id=id_object, name=name_category))
            z += 1
        except:
            e = sys.exc_info()[0]
            print("Error when creating a category: {0}".format(e))
            print('The value ' + str(category) + ' can not be index\n')
    Category.objects.bulk_create(res)
    print(str(len(res)) + ' categories indexes\n')


def import_occupations():
    print('Indexing occupations, show the progress:')
    Occupation.objects.all().delete()
    occupations = read_file('u.occupation')
    z = 0
    res = []
    for occupation in occupations:
        try:
            printProgressBar(z, len(occupations))
            occupation = str(occupation).strip()
            if occupation is not '':
                res.append(Occupation(name=str(occupation)))
            z += 1
        except:
            e = sys.exc_info()[0]
            print("Error when creating an occupation: {0}".format(e))
            print('The value ' + str(occupation) + ' can not be index\n')
    Occupation.objects.bulk_create(res)
    print(str(len(res)) + ' occupations indexes\n')


def import_users():
    print('Indexing users, show the progress:')
    User.objects.all().delete()
    users = read_file('u.user')
    res = []
    z = 0
    for user in users:
        try:
            printProgressBar(z, len(users))
            if len(user) > 0:
                id_user = int(user[0])
                age = user[1]
                sex = user[2]
                occupation = Occupation.objects.get(name=str(user[3]).strip())
                postal_code = user[4]
                res.append(User(user_id=id_user, age=age, sex=sex, occupation=occupation, postal_code=postal_code))
            z += 1
        except:
            e = sys.exc_info()[0]
            print("Error when creating an user: {0}".format(e))
            print('The value ' + str(user) + ' can not be index\n')
    User.objects.bulk_create(res)
    print(str(len(res)) + ' users indexes\n')


def import_films():
    print('Indexing films, show the progress:')
    Film.objects.all().delete()
    through_model = Film.categories.through
    films_lines = read_file('u.item')
    films = []
    relations = []
    z = 0
    for film in films_lines:
        try:
            printProgressBar(z, len(films_lines))
            film_id = int(film[0])
            title = film[1].strip()
            date = film[2].strip()
            release_date = None if len(date) == 0 else datetime.strptime(date, '%d-%b-%Y')
            imdb_url = film[4]
            films.append(Film(film_id=film_id, title=title, release_date=release_date, url=imdb_url))
            i = 5
            while i < len(film):
                aux_value = film[i].strip()
                id_category = str(i - 5)
                if '1' in aux_value:
                    category = Category.objects.get(category_id=id_category)
                    relations.append(through_model(category=category, film_id=film_id))
                i += 1
            z += 1
        except:
            e = sys.exc_info()[0]
            print("Error when creating a film: {0}".format(e))
            print('The value ' + str(film) + ' can not be index\n')
    Film.objects.bulk_create(films)
    through_model.objects.bulk_create(relations)
    print(str(z) + ' films indexes\n')


def import_punctuations():
    print('Indexing punctuations, show the progress:')
    Punctuation.objects.all().delete()
    punctuations = read_file('u.data')
    res = []
    z = 0
    for punctuation in punctuations:
        try:
            printProgressBar(z, len(punctuations))
            user_aux = punctuation[0]
            film_aux = punctuation[1]
            score = int(punctuation[2])
            res.append(Punctuation(user_id=user_aux, film_id=film_aux, rank=score))
            z += 1
        except:
            e = sys.exc_info()[0]
            print("Error when creating a punctuation: {0}".format(e))
            print('The value ' + str(punctuation) + ' can not be index\n')
    Punctuation.objects.bulk_create(res)
    print(str(len(res)) + ' punctuations indexes\n')


def import_data(selection):
    i = 0
    if 'categories' in selection:
        import_categories()
        i += 1
    if 'occupations' in selection:
        import_occupations()
        i += 1
    if 'users' in selection:
        import_users()
        i += 1
    if 'films' in selection:
        import_films()
        i += 1
    if 'punctuations' in selection:
        import_punctuations()
        i += 1
    if 'all' in selection:
        import_categories()
        import_occupations()
        import_users()
        import_films()
        import_punctuations()
        i += 4
    if i == 0:
        print('Nothing to import! Use a string array with your selection\n')
        print('It can be categories, occupations, users, film or punctuations\n')
        print("Example: ['categories', 'occupations'] or ['all'])")


#if __name__ == '__main__':
#    import_data('all')