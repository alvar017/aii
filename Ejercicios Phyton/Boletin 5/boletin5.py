from tkinter import *
from urllib import request
from tkinter import messagebox, Tk
from datetime import datetime
from bs4 import BeautifulSoup
import sqlite3 as lite
import sys


class Find:

    def find_url_aux(self, url):
        f = request.urlopen(url)
        page = f.read().decode(f.headers.get_content_charset())
        f.close()
        soup = BeautifulSoup(page, 'html.parser')
        return soup

    def find_url(self, url, number_of_pages_to_find):
        soup = self.find_url_aux(url)
        pages_query = soup.find("div", {"class": "pages margin"}).findAll("a")
        links_pages = []
        for i in range(int(number_of_pages_to_find)):
            links_pages.append(url + pages_query[i].get('href'))
        res = []
        for page in links_pages:
            res.extend(self.find_data(page))
        return res

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
    def __init__(self):
        self.find = Find()

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

    def list(self):
        self.print_with_scroll(self.find.find_db(None, None))

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

    def search_aux(self, message, objects, window):
        if len(objects) > 0:
            self.print_with_scroll(objects)
            window.destroy()
        else:
            messagebox.showinfo(message=message, title="Aviso")

    def search_box(self, selection):
        def search_pages():
            if int(txt.get()) < 5:
                self.save(self.find.find_url('https://www.meneame.net/', txt.get()))
                window.destroy()
            else:
                messagebox.showinfo(message="El número máximo de páginas es 5", title="Aviso")

        def search_author():
            authors = self.find.find_db(txt.get(), 'author')
            self.search_aux('Ninguna noticia de ese autor ha sido encontrada', authors, window)

        def search_by_date():
            news = self.find.find_db(txt.get(), 'date')
            self.search_aux('Ninguna noticia con esa fecha ha sido encontrada', news, window)

        window = Tk()
        window.title("Configuración")
        if selection == 'pages':
            question = 'Introduzca el número de páginas que desea buscar'
            btn = Button(window, text="Buscar", command=search_pages)
        elif selection == 'author':
            question = '¿Cuál es el nombre del autor a buscar?'
            btn = Button(window, text="Buscar", command=search_author)
        else:  # selection == 'date'
            question = 'Introduzca la fecha a buscar, siguiendo el formato: yyyy-mm-dd'
            btn = Button(window, text="Buscar", command=search_by_date)

        lbl = Label(window, text=question)
        lbl.pack(side=LEFT)
        txt = Entry(window)
        txt.pack(side=LEFT)
        btn.pack(side=LEFT)
        window.mainloop()

    def start(self):
        def close_window():
            root.destroy()

        window = Window()
        root = Tk()
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
