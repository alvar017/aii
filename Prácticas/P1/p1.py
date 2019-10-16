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
            answers_and_visits = threads[i].findAll("li")
            answers = answers_and_visits[0].text[-1:]
            visits = answers_and_visits[1].text[-1:]

            aux = [title, link, author, date, answers, visits]
            res.append(aux)
        return res

    def print_with_scroll(self, threads):
        res = []
        # Recuerda el orden: thread -> id, title, link, author, date, answers, visits
        for thread in threads:
            parse_date = 'Fecha: ' + dateutil.parser.parse(thread[4]).strftime("%d/%m/%Y") + '\n'
            aux = ['Título: ' + thread[1] + '\n', 'Autor: : ' + thread[3] + '\n', parse_date, '\n']
            res.append(aux)
        root = tk.Tk()
        scrollbar = tk.Scrollbar(root, orient="vertical")
        lb = tk.Listbox(root, width=190, height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=lb.yview)
        scrollbar.pack(side="right", fill="y")
        lb.pack(side="left", fill="both", expand=True)
        for i in range(len(res)):
            for z in range(len(res[i])):
                lb.insert("end", res[i][z])
        root.mainloop()

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

    def find_title(self):
        find = self.find

        def find_aux(entry):
            self.find.print_with_scroll(find.find_db(en.get(), 'title'))

        v = Toplevel()
        lb = Label(v, text="Introduzca el título del tema: ")
        lb.pack(side=LEFT)
        en = Entry(v)

        en.bind("<Return>", find_aux)
        en.pack(side=LEFT)

    def find_date(self):
        find = self.find

        def find_aux(entry):
            self.find.print_with_scroll(find.find_db(en.get(), 'date'))

        v = Toplevel()
        lb = Label(v, text="Introduzca la fecha a buscar (dia/mes/año): ")
        lb.pack(side=LEFT)
        en = Entry(v)
        en.bind("<Return>", find_aux)
        en.pack(side=LEFT)

    def start(self):
        w = Window()
        f = Find()
        top = Tk()

        menu = Menu(top)
        top.config(menu=menu)

        subMenuDatos = Menu(menu)
        menu.add_cascade(label="Datos", menu=subMenuDatos)
        subMenuDatos.add_command(label="Cargar", command=w.save)
        subMenuDatos.add_command(label="Mostrar", command=w.list)

        def close_window():
            top.destroy()

        subMenuDatos.add_command(label="Salir", command=close_window)

        subMenuBuscar = Menu(menu)
        menu.add_cascade(label="Buscar", menu=subMenuBuscar)
        subMenuBuscar.add_command(label="Tema", command=w.find_title)
        subMenuBuscar.add_command(label="Fecha", command=w.find_date)

        subMenuEstadisticas = Menu(menu)
        menu.add_cascade(label="Estadísticas", menu=subMenuEstadisticas)
        subMenuEstadisticas.add_command(label="Temas más populares", command=f.find_more_popular)
        subMenuEstadisticas.add_command(label="Temas más activos", command=f.find_more_active)
        top.mainloop()


if __name__ == "__main__":
    Window().start()

