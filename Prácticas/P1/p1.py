import tkinter as tk
from tkinter import *
from urllib import request
from tkinter import messagebox
import dateutil.parser
import sqlite3 as lite
from urllib.request import re
import sys

from bs4 import BeautifulSoup


class Busca:
    def captura_url(self, url):
        res = []                                                           # Creo lista para introducir noticias
        f = request.urlopen(url)
        captura = f.read().decode(f.headers.get_content_charset())
        f.close()

        soup = BeautifulSoup(captura, 'html.parser')
        threads = soup.findAll("li", {"class": "threadbit"})
        for i in range(len(threads)):
            titulo = threads[i].find("a", {"class": "title"}).get('title')
            enlace = 'https://foros.derecho.com/' + threads[i].find("a", {"class": "title"}).get('href')
            autor = threads[i].find("a", {"class": "username understate"}).next
            fecha = threads[i].find("a", {"class": "username understate"}).nextSibling
            respuestas_y_visitas = threads[i].findAll("li")
            respuestas = respuestas_y_visitas[0].text[-1:]
            visitas = respuestas_y_visitas[1].text[-1:]

            aux = [titulo, enlace, autor, fecha, respuestas, visitas]
            res.append(aux)
        return res

    def imprime_con_scroll(self, captura_filtrada):
        res = []
        for elemento in captura_filtrada:
            fecha_parseada = 'Fecha: ' + dateutil.parser.parse(elemento[2]).strftime("%d/%m/%Y") + '\n'
            aux = ['Título: ' + elemento[0] + '\n', 'Autor: : ' + elemento[1] + '\n', fecha_parseada, '\n']
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


class Ventana:
    def __init__(self):
        self.busca = Busca()

    def list(self):
        # Creo conexión con la base de datos
        conn = lite.connect('test.db')
        conn.text_factory = str
        # Creo cursor con la búsqueda
        cursor = conn.execute("SELECT TITULO,AUTOR,FECHA FROM hilos")
        captura_finder = []
        for row in cursor:
            captura_finder.append(row)
        conn.close()
        self.busca.imprime_con_scroll(captura_finder)

    def almacena(self):
        c = self.busca.captura_url('https://foros.derecho.com/foro/20-Derecho-Civil-General')
        con = None
        try:
            con = lite.connect('test.db')
            with con:
                cur = con.cursor()
                cur.execute("DROP TABLE IF EXISTS hilos")
                cur.execute("CREATE TABLE hilos(ID INT, TITULO TEXT, ENLACE TEXT, AUTOR TEXT, FECHA TEXT, RESPUESTAS TEXT, VISITAS TEXT)")
                for i in range(len(c)):
                    cur.execute("INSERT INTO hilos VALUES (?, ?, ?, ?, ?, ?, ?)", (i, c[i][0], c[i][1], c[i][2], c[i][3], c[i][4], c[i][5]))
        except lite.Error as e:
            print("Error {}:".format(e.args[0]))
            sys.exit(1)
        finally:
            messagebox.showinfo(message="BD creada correctamente", title="Aviso")
            if con:
                con.close()

    def buscador(self):
        def busca_db(entry):
            conn = lite.connect('test.db')
            conn.text_factory = str
            s = "%" + en.get() + "%"
            cursor = conn.execute("""SELECT TITLE,LINK,DATE FROM noticias WHERE DATE LIKE ?""", (s,))
            captura_finder = []
            for row in cursor:
                captura_finder.append(row)
            conn.close()
            self.busca.imprime_con_scroll(captura_finder)

        v = Toplevel()
        lb = Label(v, text="Introduzca el mes (Xxx): ")
        lb.pack(side=LEFT)
        en = Entry(v)
        en.bind("<Return>", busca_db)
        en.pack(side=LEFT)

    def inicia_ventana_principal(self):
        v = Ventana()
        top = Tk()

        menu = Menu(top)
        top.config(menu=menu)

        subMenuDatos = Menu(menu)
        menu.add_cascade(label="Datos", menu=subMenuDatos)
        subMenuDatos.add_command(label="Cargar", command=v.almacena)
        subMenuDatos.add_command(label="Mostrar", command=v.list)
        subMenuDatos.add_command(label="Salir")

        subMenuBuscar = Menu(menu)
        menu.add_cascade(label="Buscar", menu=subMenuBuscar)
        subMenuBuscar.add_command(label="Tema")
        subMenuBuscar.add_command(label="Fecha")

        subMenuEstadisticas = Menu(menu)
        menu.add_cascade(label="Estadísticas", menu=subMenuEstadisticas)
        subMenuEstadisticas.add_command(label="Temas más populares")
        subMenuEstadisticas.add_command(label="Temas más activos")
        top.mainloop()


if __name__ == "__main__":
    Ventana().inicia_ventana_principal()

