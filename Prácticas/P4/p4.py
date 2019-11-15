#encoding:utf-8
import locale
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
from urllib import request
import os
from datetime import datetime
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, KEYWORD, DATETIME
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser


def get_beautifulsoup(url):
    f = request.urlopen(url)
    page = f.read().decode(f.headers.get_content_charset())
    f.close()
    return BeautifulSoup(page, 'html.parser')


def find_url(url):
    res = []
    soup = get_beautifulsoup(url)
    threads = soup.find("div", {"class": "col-left"}).findAll("div", {"class": "news-card"})
    for t in threads:
        title_aux = t.find("a", {"class": "meta-title-link"})
        title = title_aux.text
        link_aux = t.find("figure", {"class": "thumbnail"}).find("img", {"class": "thumbnail-img"})
        if link_aux.get("data-src") is None:
            link = t.find("figure", {"class": "thumbnail"}).find("img", {"class": "thumbnail-img"}).get("src")
        else:
            link = t.find("figure", {"class": "thumbnail"}).find("img", {"class": "thumbnail-img"}).get("data-src")
        category = t.find("div", {"class": "meta-category"}).next
        description = t.find("div", {"class": "meta-body"})
        if description is not None:
            description = description.text
        else:
            description = get_description(title_aux.get('href'))
        locale.setlocale(locale.LC_ALL, 'esp_esp')
        date_aux = str(t.find("div", {"class": "meta-date"}).next).split(",")[1].strip()
        date = datetime.strptime(date_aux, '%d de %B de %Y')
        aux = [category, title, link, description, date]
        res.append(aux)
    return res


def get_description(url):
    soup = get_beautifulsoup("http://www.sensacine.com/" + url)
    description = soup.find("p", {"class": "article-lead"}).text
    return description


def find_url_aux(url):
    res = []
    for i in range(3):
        res.extend(find_url(url + "?page=" + str(i)))
    return res


def get_schema():
    return Schema(category=TEXT(stored=True), title=TEXT(stored=True), link=TEXT(stored=True), description=TEXT(stored=True), date=DATETIME(stored=True))


def add_doc(writer, answer):
    category = answer[0].strip()
    title = answer[1].strip()
    link = answer[2].strip()
    description = answer[3].strip()
    date = answer[4]
    writer.add_document(category=category, title=title, link=link, description=description, date=date)


def index(dir_index):
    if not os.path.exists(dir_index):
        os.mkdir(dir_index)
    ix = create_in(dir_index, schema=get_schema())
    writer = ix.writer()
    i = 0
    url = "http://www.sensacine.com/noticias/"
    news = find_url_aux(url)
    for new in news:
        if not os.path.isdir(url+new[0]):
            add_doc(writer, new)
            i += 1
    messagebox.showinfo("Fin de indexado", "Se han indexado " + str(i) + " noticias")
    writer.commit()


def get_date_query_from_input(user_input):
    date = user_input.split(" ")
    date1 = datetime.strptime(date[0], '%d/%M/%Y').strftime('%Y%M%d')
    date2 = datetime.strptime(date[1], '%d/%M/%Y').strftime('%Y%M%d')
    my_query = '{' + date1 + 'TO' + date2 + ']'
    return my_query


def get_query(schema, types, or_and, type_search, user_input):
    if or_and == 'and' and len(types) > 1:
        qp = QueryParser(types[0], schema)
        i = 0
        aux = " "
        words = user_input.split(" ")
        while i < len(types):
            if type_search:
                aux += str(types[i]) + ':"' + user_input + '" '
            else:
                for word in words:
                    aux += str(types[i]) + ":" + word + " "
            i += 1
        user_input = aux
    else:
        qp = MultifieldParser(types, schema)
    if type_search and or_and != "and":
        q = qp.parse(f'"{user_input}"')
    else:
        q = qp.parse(user_input)
    return q


def search_whoosh(types, to_save, dir_index, or_and, type_search, user_input):
    # types = en que columnas buscar
    # text = parametro de búsqueda del usuario
    # dir_index = directorio del índece
    # to_save = parametros de la tabla que se deben devolver
    # or_and = indica el tipico de búsqueda Multifieldparser, puede ser and ó or
    # type_search = indica si debe ser una búsqueda de cadena exacto o de caracteres contenidos
    res = []
    ix = open_dir(dir_index)
    with ix.searcher() as searcher:
        if types[0] == 'date':
            dates = get_date_query_from_input(user_input)
            q = get_query(ix.schema, types, or_and, type_search, dates)
        else:
            q = get_query(ix.schema, types, or_and, type_search, user_input)
        results = searcher.search(q)
        for r in results:
            aux = []
            for element in to_save:
                aux.append(r[element])
            res.append(aux)
        return res


def config_search_aux(dir_index, search, en, l):
    if en is None:
        en = ""
    else:
        en = str(en.get())
    if search == 'title':
        l.config(text='Introduzca el título a buscar')
        search_index = search_whoosh(["title", "description"], ["category", "title", "date"], dir_index, "and", False,
                                     en)
    elif search == 'description':
        l.config(text='Introduzca el texto a buscar')
        search_index = search_whoosh(["description"], ["title", "link", "description"], dir_index, "or", True,
                                     en)
    elif search == 'date':
        l.config(text='Introduzca período (dd/mm/yyyy dd/mm/yyyy)')
        search_index = search_whoosh(["date"], ["category", "title", "date"], dir_index, "or", False, en)
    return search_index


def config_search(dir_index, search):
    def mostrar_lista(event):
        lb.delete(0, END)   #borra toda la lista
        search_index = config_search_aux(dir_index, search, en, l)
        for result in search_index:
            lb.insert(END, result[0])
            lb.insert(END, result[1])
            lb.insert(END, result[2])
            lb.insert(END, " ")
    v = Toplevel()
    v.title('Búsqueda')
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text='Introduzca espacio en blanco para ver formato de búsqueda')
    l.pack(side=LEFT)
    en = Entry(f)
    config_search_aux(dir_index, search, None, l)
    en.bind("<Return>", mostrar_lista)
    en.pack(side=LEFT)
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, yscrollcommand=sc.set)
    lb.pack(side=BOTTOM, fill = BOTH)
    sc.config(command = lb.yview)


def ventana_principal():
    dirindex="Index"
    top = Tk()
    top.geometry("198x0")

    def close_window():
        top.destroy()

    menubar = Menu(top)
    top.config(menu=menubar)

    data_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Inicio", menu=data_menu)
    data_menu.add_command(label="Indexar", command=lambda: index(dirindex))
    data_menu.add_separator()
    data_menu.add_command(label="Salir", command=close_window)

    data_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Buscar", menu=data_menu)
    data_menu.add_command(label="Título y Descripción", command=lambda: config_search(dirindex, 'title'))
    data_menu.add_command(label="Fecha", command=lambda: config_search(dirindex, 'date'))
    data_menu.add_command(label="Descripción", command=lambda: config_search(dirindex, 'description'))

    top.mainloop()


if __name__ == '__main__':
    ventana_principal()