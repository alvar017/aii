from tkinter import *
from urllib import request
from tkinter import messagebox, Tk
from datetime import datetime
from bs4 import BeautifulSoup
import sqlite3 as lite
import sys


class Find:
    # Devuelve un objeto beautifulsoup de la URL dada
    def find_url_aux(self, url):
        f = request.urlopen(url)
        page = f.read().decode(f.headers.get_content_charset())
        f.close()
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    # Dada una URL devuelve todas las noticias de una URL (teniendo en cuenta el número de páginas solicitadas por el usuario)
    def find_url(self, url, pages_number):
        soup = self.find_url_aux(url)
        pages_query = soup.find("div", {"class": "pages margin"}).findAll("a")
        links_pages = []
        for i in range(int(pages_number)):
            links_pages.append(url + pages_query[i].get('href'))
        res = []
        for page in links_pages:
            res.extend(self.find_data(page))
        return res

    # Busca los datos solicitados por el enunciado y los devuelve en una lista
    def find_data(self, link):
        res = []
        page = self.find_url_aux(link)
        news = page.findAll("div", {"class": "news-summary"})
        for i in range(len(news)):
            title = news[i].find("h2").find("a").text
            link = news[i].find("h2").find("a").get('href')
            author = news[i].find("div", {"class": "news-submitted"}).findAll("a")[1].text
            date = int(news[i].find("span", {"class": "ts visible"}).get('data-ts'))
            date_parse = datetime.fromtimestamp(date)
            content = news[i].find("div", {"class": "news-content"}).text
            aux = [title, link, author, date_parse, content]
            res.append(aux)
        return res

    # Búsqueda en la base de datos en función de una palabra clave (en) y una categoría
    def find_db(self, en, category):
        conn = lite.connect('test.db')
        conn.text_factory = str
        if en is not None:
            s = "%" + en + "%"
            if category == 'author':
                cursor = conn.execute("SELECT * FROM news WHERE author LIKE ?", (s,))
            elif category == 'date':
                cursor = conn.execute("SELECT * FROM news WHERE date LIKE ?", (s,))
        else:
            cursor = conn.execute("SELECT * FROM news")
        res = []
        for row in cursor:
            res.append(row)
        conn.close()
        return res


class Window:
    find = Find()

    # Dado un conjunto de noticias devuelve una listbox con estas
    def print_with_scroll(self, threads):
        res = []
        # Order: thread -> id, title, link, author, date, answers, visits
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

    # Crea una listbox con todas las noticias de la listbox
    def list(self):
        self.print_with_scroll(self.find.find_db(None, None))

    # Guarda el conjunto de datos pasados como parámetro
    def save(self, objects):
        c = objects
        con = None
        try:
            # aux = [title, link, author, date_parse, content]
            con = lite.connect('test.db')
            with con:
                cur = con.cursor()
                cur.execute("DROP TABLE IF EXISTS news")
                cur.execute("CREATE TABLE news(ID INT, TITLE TEXT, LINK TEXT, AUTHOR TEXT, DATE TEXT, CONTENT TEXT)")
                for i in range(len(c)):
                    cur.execute("INSERT INTO news VALUES (?, ?, ?, ?, ?, ?)", (i, c[i][0], c[i][1], c[i][2], c[i][3], c[i][4]))
                messagebox.showinfo(message="BD creada correctamente con " + str(len(c)) + " respuestas", title="Aviso")
        except lite.Error as e:
            print("Error {}:".format(e.args[0]))
            messagebox.showinfo(message="Se ha producido un error", title="Aviso")
            sys.exit(1)
        finally:
            if con:
                con.close()

    # Crea una listbox en caso de encontrar resultados, un aviso en caso de no encontrar nada
    def search_aux(self, message, objects, window):
        if len(objects) > 0:
            self.print_with_scroll(objects)
            window.destroy()
        else:
            messagebox.showinfo(message=message, title="Aviso")

    # Crea un cuadro de búsqueda en función del tipo elegido
    def search_box(self, selection):
        def search():
            if selection == 'pages':
                if 0 < int(entry.get()) < 5:
                    self.save(self.find.find_url('https://www.meneame.net/', entry.get()))
                    window.destroy()
                else:
                    messagebox.showinfo(message="El número de páginas debe estar entre 1 y 4", title="Aviso")
            elif selection == 'author':
                authors = self.find.find_db(entry.get(), 'author')
                self.search_aux('Ninguna noticia de ese autor ha sido encontrada', authors, window)
            else:
                news = self.find.find_db(entry.get(), 'date')
                self.search_aux('Ninguna noticia con esa fecha ha sido encontrada', news, window)

        window = Tk()
        window.title("Configuración")
        if selection == 'pages':
            question = 'Introduzca el número de páginas que desea buscar'
        elif selection == 'author':
            question = '¿Cuál es el nombre del autor a buscar?'
        else:  # selection == 'date'
            question = 'Introduzca la fecha a buscar, siguiendo el formato: yyyy-mm-dd'

        button = Button(window, text="Buscar", command=search)
        label = Label(window, text=question)
        label.pack(side=LEFT)
        entry = Entry(window)
        entry.pack(side=LEFT)
        button.pack(side=LEFT)
        window.mainloop()

    def start(self):
        def close_window():
            root.destroy()

        window = Window()
        root = Tk()
        root.geometry("198x0")
        menubar = Menu(root)
        root.config(menu=menubar)

        data_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Datos", menu=data_menu)
        data_menu.add_command(label="Cargar", command=lambda: self.search_box('pages'))
        data_menu.add_command(label="Mostrar", command=window.list)
        data_menu.add_separator()
        data_menu.add_command(label="Salir", command=close_window)

        find_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Buscar", menu=find_menu)
        find_menu.add_command(label="Por nombre de autor", command=lambda: self.search_box('author'))
        find_menu.add_command(label="Por fecha", command=lambda: self.search_box('date'))

        root.mainloop()


if __name__ == "__main__":
    Window().start()
