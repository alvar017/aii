import tkinter as tk
from tkinter import *
from urllib import request
from tkinter import messagebox, Tk
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
        res = []
        threads = soup.findAll("div", {"class": "cont-modulo resultados"})
        for i in range(len(threads)):
            session = threads[i].text[1:22]
            matches = threads[i].findAll("tr")
            for e in range(len(matches)):
                if e is not 0:
                    match = matches[e].findAll('td')[1].find('a').get('title')[0:-11]
                    result = matches[e].findAll('td')[1].find('a').next[0:-1].strip(' ')
                    link = 'https://resultados.as.com' + matches[e].findAll('td')[1].find('a').get('href')
                    aux = [session, match, result, link]
                    res.append(aux)
        return res

    def print_with_scroll(self, threads):
        res = []
        # Recuerda el orden: thread -> id, title, link, author, date, answers, visits
        for thread in threads:
            aux = [thread[1] + '\n', 'Partido: ' + thread[2] + '\n', 'Resultado: ' + thread[3] + '\n', 'Link: ' + thread[4] + '\n', '\n']
            res.append(aux)

        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, yscrollcommand=sc.set)
        for row in res:
            lb.insert(END, row[0])
            lb.insert(END, row[1])
            lb.insert(END, row[2])
            lb.insert(END, row[3])
            lb.insert(END, '')
        lb.pack(side=LEFT, fill=BOTH)
        sc.config(command=lb.yview)

    def find_db(self):
        conn = lite.connect('test.db')
        conn.text_factory = str
        cursor = conn.execute("SELECT * FROM matches")
        res = []
        for row in cursor:
            res.append(row)
        conn.close()
        return res


class Window:
    def __init__(self):
        self.find = Find()

    def list(self):
        self.find.print_with_scroll(self.find.find_db())

    def save(self):
        c = self.find.find_url('https://resultados.as.com/resultados/futbol/primera/2018_2019/calendario/')
        con = None
        try:
            con = lite.connect('test.db')
            with con:
                cur = con.cursor()
                cur.execute("DROP TABLE IF EXISTS matches")
                cur.execute("CREATE TABLE matches(ID INT, SESSION TEXT, MATCH TEXT, RESULT TEXT, LINK TEXT)")
                for i in range(len(c)):
                    cur.execute("INSERT INTO matches VALUES (?, ?, ?, ?, ?)", (i, c[i][0], c[i][1], c[i][2], c[i][3]))
                messagebox.showinfo(message="BD creada correctamente con " + str(len(c)) + " partidos", title="Aviso")
        except lite.Error as e:
            print("Error {}:".format(e.args[0]))
            messagebox.showinfo(message="Se ha producido un error", title="Aviso")
            sys.exit(1)
        finally:
            if con:
                con.close()

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

        root.mainloop()


if __name__ == "__main__":
    Window().start()
