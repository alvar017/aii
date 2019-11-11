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


def find_url(url):
    res = []
    f = request.urlopen(url)
    page = f.read().decode(f.headers.get_content_charset())
    f.close()

    soup = BeautifulSoup(page, 'html.parser')
    threads = soup.find("div", {"class": "col-left"}).findAll("div", {"class": "news-card"})
    for t in threads:
        title = t.find("a", {"class": "meta-title-link"}).next
        link_aux = t.find("figure", {"class": "thumbnail"}).find("img", {"class": "thumbnail-img"})
        if link_aux.get("data-src") is None:
            link = t.find("figure", {"class": "thumbnail"}).find("img", {"class": "thumbnail-img"}).get("src")
        else:
            link = t.find("figure", {"class": "thumbnail"}).find("img", {"class": "thumbnail-img"}).get("data-src")
        categoria = t.find("div", {"class": "meta-category"}).next
        descripcion = t.find("div", {"class": "meta-body"})
        if descripcion != None:
            descripcion = descripcion.text
        else:
            descripcion = ""
        locale.setlocale(locale.LC_ALL, 'esp_esp')
        date_aux = str(t.find("div", {"class": "meta-date"}).next).split(",")[1].strip()
        date = datetime.strptime(date_aux, '%d de %B de %Y')
        aux = [categoria, title, link, descripcion, date]
        res.append(aux)
    return res


def find_url_aux(url):
    res = []
    pages = [1, 2, 3]
    for i in pages:
        res.extend(find_url(url + "?page=" + str(i)))
    return res


def get_schema_thread():
    return Schema(category=TEXT(stored=True), title=TEXT(stored=True), link=TEXT(stored=True), description=TEXT(stored=True), date=DATETIME(stored=True))


def add_doc(writer, answer):
    category = answer[0].strip()
    title = answer[1].strip()
    link = answer[2].strip()
    description = answer[3].strip()
    date = answer[4]

    writer.add_document(category=category, title=title, link=link, description=description, date=date)


def apartado_a(dirindex):
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)

    ix = create_in(dirindex, schema=get_schema_thread())
    writer = ix.writer()
    i = 0
    url = "http://www.sensacine.com/noticias/"
    answers = find_url_aux(url)
    for answer in answers:
        if not os.path.isdir(url+answer[0]):
            add_doc(writer, answer)
            i += 1
    messagebox.showinfo("Fin de indexado", "Se han indexado " + str(i) + " temas")
            
    writer.commit()


def apartado_b(dirindex, search):
    def mostrar_lista(event):
        lb.delete(0,END)   #borra toda la lista
        ix=open_dir(dirindex)      
        with ix.searcher() as searcher:
            query = QueryParser(search, ix.schema).parse(str(en.get()))
            results = searcher.search(query)
            for r in results:
                lb.insert(END,r['title'])
                lb.insert(END,r['author'])
                lb.insert(END, r['date'])
                lb.insert(END,'')
    
    v = Toplevel()
    if (search == 'title'):
        ref = 'Introduzca el título a buscar'
    elif (search == 'author'):
        ref = 'Introduzca el nombre del autor'
    else:
        ref = 'Búsqueda'
    v.title('Búsqueda')
    f =Frame(v)
    f.pack(side=TOP)
    l = Label(f, text=ref)
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
    menubar.add_cascade(label="Inicio", menu=data_menu)
    data_menu.add_command(label="Indexar", command=lambda: apartado_a(dirindex))
    data_menu.add_separator()
    data_menu.add_command(label="Salir", command=close_window)

    data_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Buscar", menu=data_menu)
    data_menu.add_command(label="Título", command=lambda: apartado_b(dirindex, 'title'))
    data_menu.add_command(label="Autor", command=lambda: apartado_b(dirindex, 'author'))

    top.mainloop()


if __name__ == '__main__':
    ventana_principal()