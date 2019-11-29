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
    threads = soup.findAll("div", {"class": "cal_info clearfix"})
    for t in threads:
        title = t.find("span", {"class": "summary"}).text

        description = t.find("p", {"class": "description"})
        if description is None:
            description = "No tiene descripción"
        else:
            description = description.text

        categoria = ""
        categoria_aux = t.find("li", {"class": "category"})
        if categoria_aux is None:
            categoria = "No tiene categoría"
        else:
            categoria_aux1 = categoria_aux.findAll("span")
            for c in categoria_aux1:
                categoria = categoria + " " + c.text

        date_all = t.find("div", {"class": "documentByLine"}).findAll("abbr")
        if len(date_all) == 0:
            date_start_aux = t.find("div", {"class": "documentByLine"}).text
            date_start = date_start_aux
            date_start = date_start.replace(" ", "")
            date_start = date_start.replace("\n", "")[0:10]
            date_end = "No tiene fecha fin"
        else:
            if len(date_all) == 1:
                date_start_aux = date_all[0].get("title")
                date_start = date_start_aux[0:10]
                date_end = "No tiene fecha fin"
            else:
                date_start_aux = date_all[0].get("title")
                date_end_aux = date_all[1].get("title")

                date_start = date_start_aux[0:10]
                date_end = date_end_aux[0:10]

        aux = [title, date_start, date_end, description, categoria]
        res.append(aux)
    return res


def find_url_aux(url):
    res = []
    for i in range(1):
        res.extend(find_url(url + "?page=" + str(i)))
    return res


def get_schema():
    return Schema(title=TEXT(stored=True), date_start=DATETIME(stored=True), date_end=DATETIME(stored=True),
                  description=TEXT(stored=True), categoria=TEXT(stored=True))


def add_doc(writer, answer):
    title = answer[0].strip()
    if answer[2] in "No tiene fecha fin":
        if "/" in answer[1]:
            date_start = datetime.strptime(answer[1], '%d/%m/%Y')
        else:
            date_start = datetime.strptime(answer[1], '%Y-%m-%d')
        date_end = date_start
    else:
        date_start = datetime.strptime(answer[1], '%Y-%m-%d')
        date_end = datetime.strptime(answer[2].strip(), '%Y-%m-%d')
    description = answer[3].strip()
    categoria = answer[4]
    writer.add_document(title=title, date_start=date_start, date_end=date_end, description=description,
                        categoria=categoria)


def index(dir_index):
    if not os.path.exists(dir_index):
        os.mkdir(dir_index)
    ix = create_in(dir_index, schema=get_schema())
    writer = ix.writer()
    i = 0
    url = "https://www.sevilla.org/ayuntamiento/alcaldia/comunicacion/calendario/agenda-actividades"
    news = find_url_aux(url)
    for new in news:
        if not os.path.isdir(url + new[0]):
            add_doc(writer, new)
            i += 1
    messagebox.showinfo("Fin de indexado", "Se han indexado " + str(i) + " noticias")
    writer.commit()


def get_date_query_from_input(user_input):
    locale.setlocale(locale.LC_ALL, 'esp_esp')
    user_input = user_input.replace("Ene", "1")
    user_input = user_input.replace("Feb", "2")
    user_input = user_input.replace("Mar", "3")
    user_input = user_input.replace("Abr", "4")
    user_input = user_input.replace("May", "5")
    user_input = user_input.replace("Jun", "6")
    user_input = user_input.replace("Jul", "7")
    user_input = user_input.replace("Ago", "8")
    user_input = user_input.replace("Sep", "9")
    user_input = user_input.replace("Oct", "10")
    user_input = user_input.replace("Nov", "11")
    user_input = user_input.replace("Dic", "12")
    date = datetime.strptime(user_input, '%d de %m de %Y').strftime('%Y%m%d')
    my_query = '{TO' + date + ']'
    return my_query


# Obtiene el conjunto de elementos a seleccionar en función de la categoría
def spin_box_aux(dir_index):
    res = []
    ix = open_dir(dir_index)
    with ix.searcher() as searcher:
        qp = QueryParser('categoria', ix.schema)
        q = qp.parse("categoria:' '")
    results = searcher.search(q)
    for r in results:
        res.append(r)
    res.sort()
    res.remove(res[0])
    return res


# Crea una spin box con los elementos de la categoria dada
# Para que funcoine hay que añadir en spin_box_aux y en find_db los correspondientes if y elseif para ajustar la configuración
def spin_box(dir_index):
    # Búsqueda final de elemnto, cogemos el elemento seleccionado por el usuario
    def search():
        res = []
        ix = open_dir(dir_index)
        with ix.searcher() as searcher:
            qp = QueryParser('categoria', ix.schema)
            q = qp.parse(" ")
        results = searcher.search(q)
        for r in results:
            lb.insert(END, r[0])
            lb.insert(END, r[1])
            lb.insert(END, r[2])
            lb.insert(END, " ")

    elements = spin_box_aux(dir_index)
    if len(elements) > 0:
        master = Tk()
        lb = Spinbox(master, values=elements, width=10)
        lb.pack()
        button = Button(master, text='Buscar', command=search)
        button.pack(side=LEFT)
        master.mainloop()
    else:
        messagebox.showinfo(message='No hay elementos suficientes para realizar la búsqueda', title="Aviso")


def get_query(schema, types, or_and, type_search, user_input, dir_index):
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
        if types[0] == 'date_end':
            dates = get_date_query_from_input(user_input)
            q = get_query(ix.schema, types, or_and, type_search, dates, dir_index)
        elif types[0] == 'category':
            categories = spin_box(dir_index)
        else:
            q = get_query(ix.schema, types, or_and, type_search, user_input, dir_index)
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
        search_index = search_whoosh(["title", "description"], ["title", "date_start", "date_end"], dir_index, "and", False,
                                     en)
    elif search == 'description':
        l.config(text='Introduzca el texto a buscar')
        search_index = search_whoosh(["description"], ["title", "link", "description"], dir_index, "or", True,
                                     en)
    elif search == 'date':
        l.config(text='Introduzca fecha máxima de búsqueda')
        search_index = search_whoosh(["date_end"], ["title", "date_start", "date_end"], dir_index, "or", False, en)
    elif search == 'category':
        l.config(text='Elija categoría')
        search_index = search_whoosh(["category"], ["category", "title", "date"], dir_index, "or", False, en)
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
    menubar.add_cascade(label="Datos", menu=data_menu)
    data_menu.add_command(label="Cargar", command=lambda: index(dirindex))
    data_menu.add_separator()
    data_menu.add_command(label="Salir", command=close_window)

    data_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Buscar", menu=data_menu)
    data_menu.add_command(label="Título y Descripción", command=lambda: config_search(dirindex, 'title'))
    data_menu.add_command(label="Fecha", command=lambda: config_search(dirindex, 'date'))
    data_menu.add_command(label="Elija categoría", command=lambda: spin_box(dirindex))

    top.mainloop()


if __name__ == '__main__':
    ventana_principal()