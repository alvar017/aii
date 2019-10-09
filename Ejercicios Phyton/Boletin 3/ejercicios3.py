import tkinter as tk
from tkinter import *
from urllib import request
from urllib.request import re
from tkinter import messagebox
import dateutil.parser
import sqlite3 as lite
import sys


class Busca:
    def captura_url(self, url, filtro):
        res = []                                                           # Creo lista para introducir noticias
        f = request.urlopen(url)
        captura = f.read().decode(f.headers.get_content_charset())
        f.close()
        captura_filtrada = re.findall(filtro, captura)                     # Elimino de la captura lo que no coincide con la búsqueda
        for elemento in captura_filtrada:
            aux = [elemento[0], elemento[1], elemento[2], elemento[3]]     # Creo una noticia
            res.append(aux)
        return res

    def imprime_con_scroll(self, captura_filtrada):
        res = []
        for elemento in captura_filtrada:
            fecha_parseada = 'Fecha: ' + dateutil.parser.parse(elemento[2]).strftime("%d/%m/%Y") + '\n'
            aux = ['Título: ' + elemento[0] + '\n', 'Link: ' + elemento[1] + '\n', fecha_parseada, '\n']
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
        cursor = conn.execute("SELECT TITLE,LINK,DATE FROM noticias WHERE DATE LIKE ?", ('%%',))
        captura_finder = []
        for row in cursor:
            captura_finder.append(row)
        conn.close()
        self.busca.imprime_con_scroll(captura_finder)

    def almacena(self):
        captura_impresa = self.busca.captura_url('http://www.us.es/rss/feed/portada', r'<item>\s*<title>(.*)</title>\s*<link>(.*)</link>\s*<description>.*</description>\s*<author>.*</author>\s*(<category>.*</category>)?\s*<guid.*</guid>\s*<pubDate>(.*)</pubDate>\s*</item>')
        con = None
        try:
            con = lite.connect('test.db')
            with con:
                cur = con.cursor()
                cur.execute("DROP TABLE IF EXISTS noticias")
                cur.execute("CREATE TABLE noticias(ID INT, TITLE TEXT, LINK TEXT, DATE TEXT)")
                for i in range(len(captura_impresa)):
                    cur.execute("INSERT INTO noticias VALUES (?, ?, ?, ?)", (i, captura_impresa[i][0], captura_impresa[i][1], captura_impresa[i][3]))
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
        top = tk.Tk()
        button_almacenar = Button(top, text="Almacenar", command=v.almacena)
        button_almacenar.pack(side=tk.LEFT)
        button_list = Button(top, text="Listar", command=v.list)
        button_list.pack(side=tk.LEFT)
        button_buscar = Button(top, text="Buscar", command=v.buscador)
        button_buscar.pack(side=tk.LEFT)
        top.mainloop()


if __name__ == "__main__":
    Ventana().inicia_ventana_principal()

