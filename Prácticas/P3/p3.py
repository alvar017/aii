#encoding:utf-8
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
from urllib import request
import os
import dateutil.parser
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.qparser import QueryParser


def find_url(url):
    res = []
    f = request.urlopen(url)
    page = f.read().decode(f.headers.get_content_charset())
    f.close()

    soup = BeautifulSoup(page, 'html.parser')
    threads = soup.findAll("li", {"class": "threadbit"})
    for i in range(len(threads)):
        title = threads[i].find("a", {"class": "title"}).get('title')
        link = 'https://foros.derecho.com/' + threads[i].find("a", {"class": "title"}).get('href')
        author = threads[i].find("a", {"class": "username understate"}).next
        date = threads[i].find("a", {"class": "username understate"}).nextSibling.string[2:]
        date_parse = dateutil.parser.parse(date).strftime("%d/%m/%Y")
        answers_and_visits = threads[i].findAll("li")
        answers = answers_and_visits[0].text[-1:]
        visits = answers_and_visits[1].text[-1:]

        aux = [title, link, author, date_parse, answers, visits]
        res.append(aux)
    return res


def find_url_response(url):
    res = []
    f = request.urlopen(url)
    page = f.read().decode(f.headers.get_content_charset())
    f.close()

    soup = BeautifulSoup(page, 'html.parser')
    threads = soup.findAll("li", {"class": "threadbit"})
    for i in range(len(threads)):
        title = threads[i].find("a", {"class": "title"}).get('title')
        link = 'https://foros.derecho.com/' + threads[i].find("a", {"class": "title"}).get('href')
        author = threads[i].find("a", {"class": "username understate"}).next
        date = threads[i].find("a", {"class": "username understate"}).nextSibling.string[2:]
        date_parse = dateutil.parser.parse(date).strftime("%d/%m/%Y")
        answers_and_visits = threads[i].findAll("li")
        answers = answers_and_visits[0].text[-1:]
        visits = answers_and_visits[1].text[-1:]

        aux = [title, link, author, date_parse, answers, visits]
        res.append(aux)
    return res


def apartado_a(dirindex):
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)

    ix = create_in(dirindex, schema=get_schema_thread())
    writer = ix.writer()
    i=0
    url = "https://foros.derecho.com/foro/34-Derecho-Inmobiliario"
    answers = find_url(url)
    responses = []
    for answer in answers:
        responses.append(find_url_response(answer[1]))
        if not os.path.isdir(url+answer[0]):
            add_doc(writer, answer)
            i+=1
    messagebox.showinfo("Fin de indexado", "Se han indexado "+str(i)+ " temas")
            
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


def get_schema_thread():
    return Schema(title=KEYWORD(stored=True), link=TEXT(stored=True), author=TEXT(stored=True), date=TEXT(stored=True), answers=TEXT(stored=True), visits=TEXT(stored=True))


def get_schema_answers():
    return Schema(link=TEXT(stored=True), date=TEXT(stored=True), response=TEXT(stored=True), author=KEYWORD(stored=True))


def add_doc(writer, answer):
    title = answer[0].strip()
    link = answer[1].strip()
    author = answer[2].strip()
    date = answer[3].strip()
    answers = answer[4].strip()
    visits = answer[5].strip()
    
    writer.add_document(title=title, link=link, author=author, date=date, answers=answers, visits=visits)

    
def ventana_principal():
    dirindex="C:/Users/Alvaro/OneDrive - UNIVERSIDAD DE SEVILLA/AII/aii/Ejercicios Phyton/Boletin 6/Index"
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