import tkinter as tk
from tkinter import *
from urllib import request
from tkinter import messagebox
import dateutil.parser
import sqlite3 as lite
import sys

from bs4 import BeautifulSoup


class Find:
    def find_url(self, url):
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

    def print_with_scroll(self, threads):
        res = []
        # Recuerda el orden: thread -> id, title, link, author, date, answers, visits
        for thread in threads:
            aux = ['Título: ' + thread[1] + '\n', 'Autor: : ' + thread[3] + '\n', 'Fecha: ' + thread[4] + '\n', '\n']
            res.append(aux)

        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, yscrollcommand=sc.set)
        for row in res:
            lb.insert(END, row[0])
            lb.insert(END, row[1])
            lb.insert(END, row[2])
            lb.insert(END, '')
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command=lb.yview)

    def find_more_popular(self):
        threads = self.find_db(None, None)
        threads.sort(reverse=True, key=lambda thread: int(thread[6]))
        self.print_with_scroll(threads[0:5])

    def find_more_active(self):
        threads = self.find_db(None, None)
        threads.sort(reverse=True, key=lambda thread: int(thread[5]))
        self.print_with_scroll(threads[0:5])

    def find_db(self, en, category):
        conn = lite.connect('test.db')
        conn.text_factory = str
        if en is not None:
            s = "%" + en + "%"
            if category == 'title':
                cursor = conn.execute("SELECT * FROM hilos WHERE TITULO LIKE ?", (s,))
            elif category == 'date':
                cursor = conn.execute("SELECT * FROM hilos WHERE FECHA LIKE ?", (s,))
        else:
            cursor = conn.execute("SELECT * FROM hilos")
        res = []
        for row in cursor:
            res.append(row)
        conn.close()
        return res


class Window:
    def __init__(self):
        self.find = Find()

    def list(self):
        self.find.print_with_scroll(self.find.find_db(None, None))

    def save(self):
        c = self.find.find_url('https://foros.derecho.com/foro/20-Derecho-Civil-General')
        con = None
        try:
            con = lite.connect('test.db')
            with con:
                cur = con.cursor()
                cur.execute("DROP TABLE IF EXISTS hilos")
                cur.execute("CREATE TABLE hilos(ID INT, TITULO TEXT, ENLACE TEXT, AUTOR TEXT, FECHA TEXT, RESPUESTAS TEXT, VISITAS TEXT)")
                for i in range(len(c)):
                    cur.execute("INSERT INTO hilos VALUES (?, ?, ?, ?, ?, ?, ?)", (i, c[i][0], c[i][1], c[i][2], c[i][3], c[i][4], c[i][5]))
                messagebox.showinfo(message="BD creada correctamente con " + str(len(c)) + " respuestas", title="Aviso")
        except lite.Error as e:
            print("Error {}:".format(e.args[0]))
            messagebox.showinfo(message="Se ha producido un error", title="Aviso")
            sys.exit(1)
        finally:
            if con:
                con.close()

    def create_search_box(self, question, category):
        find = self.find

        v = Toplevel()
        lb = Label(v, text=question)
        lb.pack(side=LEFT)
        en = Entry(v)

        def find_aux(entry):
            if category == 'title':
                self.find.print_with_scroll(find.find_db(en.get(), 'title'))
            else:
                self.find.print_with_scroll(find.find_db(en.get(), 'date'))

        en.bind("<Return>", find_aux)
        en.pack(side=LEFT)

        return en

    def find_title(self):
        self.create_search_box('Intoduzca título del tema', 'title')

    def find_date(self):
        self.create_search_box('Introduzca la fecha a buscar (dia/mes/año): ', 'date')

    def start(self):
        window = Window()
        find = Find()

        root = Tk()
        menubar = Menu(root)
        root.config(menu=menubar)

        data_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datos", menu=data_menu)
        data_menu.add_command(label="Cargar", command=window.save)
        data_menu.add_command(label="Mostrar", command=window.list)
        data_menu.add_separator()

        def close_window():
            root.destroy()

        data_menu.add_command(label="Salir", command=close_window)

        subMenuBuscar = Menu(menubar)
        menubar.add_cascade(label="Buscar", menu=subMenuBuscar)
        subMenuBuscar.add_command(label="Tema", command=window.find_title)
        subMenuBuscar.add_command(label="Fecha", command=window.find_date)

        subMenuEstadisticas = Menu(menubar)
        menubar.add_cascade(label="Estadísticas", menu=subMenuEstadisticas)
        subMenuEstadisticas.add_command(label="Temas más populares", command=find.find_more_popular)
        subMenuEstadisticas.add_command(label="Temas más activos", command=find.find_more_active)

        root.mainloop()


if __name__ == "__main__":
    Window().start()
