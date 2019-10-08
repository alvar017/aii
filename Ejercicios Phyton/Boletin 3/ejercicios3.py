import tkinter as tk
from tkinter import *
from urllib import request
from urllib.request import re
import dateutil.parser
from tkinter import messagebox


class Busca:
    def capturar(self, url):
        f = request.urlopen(url)
        captura = f.read().decode(f.headers.get_content_charset())
        f.close()
        return captura

    def filtra(self, filtro, captura):
        return re.findall(filtro, captura)

    def imprime(self, captura_filtrada):
        a = []
        for elemento in captura_filtrada:
            s = ''
            s = s + 'Título: ' + elemento[0] + "\n"
            s = s + 'Link: ' + elemento[1] + "\n"
            s = s + 'Fecha: ' + dateutil.parser.parse(elemento[3]).strftime("%d/%m/%Y") + '\n' + '\n'
            a.append(s)
        return a


class Ventana:

    def __init__(self):
        top = tk.Tk()

        def list():
            busca = Busca()
            captura = busca.capturar('http://www.us.es/rss/feed/portada')
            captura_filtrada = busca.filtra(r'<item>\s*<title>(.*)</title>\s*<link>(.*)</link>\s*<description>.*</description>\s*<author>.*</author>\s*(<category>.*</category>)?\s*<guid.*</guid>\s*<pubDate>(.*)</pubDate>\s*</item>', captura)

            master = tk.Tk()
            master.geometry("300x300")
            master.maxsize(4000000000, 600)

            scrollbar = Scrollbar(master)
            scrollbar.pack(side=RIGHT, fill=Y)

            listbox = Listbox(master, yscrollcommand=scrollbar.set)
            for i in range(len(busca.imprime(captura_filtrada))):
                listbox.insert(END, str(busca.imprime(captura_filtrada)[i]))
            listbox.pack(side=LEFT, fill=BOTH)

            scrollbar.config(command=listbox.yview())
#            messagebox.showinfo("List", busca.imprime(captura_filtrada))







        B = Button(top, text ="Almacenar")
        B.pack(side=tk.LEFT)

        C = Button(top, text ="Listar", command = list)
        C.pack(side=tk.LEFT)

        D = Button(top, text ="Buscar")
        D.pack(side=tk.LEFT)

        top.mainloop()


if __name__ == "__main__":
    ventana = Ventana()
