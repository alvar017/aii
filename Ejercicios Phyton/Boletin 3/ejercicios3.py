import tkinter as tk
from tkinter import *
from urllib import request
from urllib.request import re
from tkinter import  messagebox
import dateutil.parser
import sqlite3 as lite
import sys


class Busca:
    def capturar(self, url):
        f = request.urlopen(url)
        captura = f.read().decode(f.headers.get_content_charset())
        f.close()
        return captura

    def filtra(self, filtro, captura):
        return re.findall(filtro, captura)

    def imprime(self, captura_filtrada):
        res = []
        for elemento in captura_filtrada:
            aux = ['Título: ' + elemento[0] + '\n', 'Link: ' + elemento[1] + '\n',
                   'Fecha: ' + dateutil.parser.parse(elemento[3]).strftime("%d/%m/%Y") + '\n', '\n']
            res.append(aux)
        return res

    def imprime_url_filtro(self, url, filtro):
        busca = Busca()
        captura = busca.capturar(url)
        captura_filtrada = busca.filtra(filtro, captura)
        captura_impresa = busca.imprime(captura_filtrada)
        return captura_impresa


class Ventana:
    def __init__(self):
        def list():
            busca = Busca()
            captura_impresa = busca.imprime_url_filtro('http://www.us.es/rss/feed/portada', r'<item>\s*<title>(.*)</title>\s*<link>(.*)</link>\s*<description>.*</description>\s*<author>.*</author>\s*(<category>.*</category>)?\s*<guid.*</guid>\s*<pubDate>(.*)</pubDate>\s*</item>')

            root = tk.Tk()
            scrollbar = tk.Scrollbar(root, orient="vertical")
            lb = tk.Listbox(root, width=190, height=20, yscrollcommand=scrollbar.set)
            scrollbar.config(command=lb.yview)

            scrollbar.pack(side="right", fill="y")
            lb.pack(side="left", fill="both", expand=True)
            for i in range(len(captura_impresa)):
                for z in range(len(captura_impresa[i])):
                    lb.insert("end", captura_impresa[i][z])
            root.mainloop()

        def almacena():
            busca = Busca()
            captura_impresa = busca.imprime_url_filtro('http://www.us.es/rss/feed/portada', r'<item>\s*<title>(.*)</title>\s*<link>(.*)</link>\s*<description>.*</description>\s*<author>.*</author>\s*(<category>.*</category>)?\s*<guid.*</guid>\s*<pubDate>(.*)</pubDate>\s*</item>')

            con = None
            try:
                con = lite.connect('test.db')
                with con:
                    cur = con.cursor()
                    cur.execute("DROP TABLE IF EXISTS noticias")
                    cur.execute("CREATE TABLE noticias(id INT, title TEXT, link TEXT, date TEXT)")
                    for i in range(len(captura_impresa)):
                        cur.execute("INSERT INTO noticias VALUES (?, ?, ?, ?)", (i, captura_impresa[i][0], captura_impresa[i][1], captura_impresa[i][2]))

#                    cur = con.cursor()
#                    cur.execute("SELECT * FROM noticias")
#                    rows = cur.fetchall()
#                    for row in rows:
#                        print(row)
            except lite.Error as e:
                print("Error {}:".format(e.args[0]))
                sys.exit(1)
            finally:
                messagebox.showinfo(message="BD creada correctamente", title="Aviso")
                if con:
                    con.close()

        top = tk.Tk()

        button_almacenar = Button(top, text="Almacenar", command=almacena)
        button_almacenar.pack(side=tk.LEFT)

        button_list = Button(top, text="Listar", command=list)
        button_list.pack(side=tk.LEFT)

        button_buscar = Button(top, text="Buscar")
        button_buscar.pack(side=tk.LEFT)

        top.mainloop()


if __name__ == "__main__":
    ventana = Ventana()
