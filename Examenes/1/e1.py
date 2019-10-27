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
        for new in news:
            title = new.find("h2").find("a").text
            link = new.find("h2").find("a").get('href')
            author = new.find("div", {"class": "news-submitted"}).findAll("a")[1].text
            date = int(new.find("span", {"class": "ts visible"}).get('data-ts'))
            date_parse = datetime.fromtimestamp(date)
            content = new.find("div", {"class": "news-content"}).text
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
            elif category == 'author_elements':
                cursor = conn.execute("SELECT AUTHOR FROM news")
            elif category == 'dates_elements':
                cursor = conn.execute("SELECT DATE FROM news")
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
        con = None
        try:
            # aux = [title, link, author, date_parse, content]
            con = lite.connect('test.db')
            with con:
                cur = con.cursor()
                cur.execute("DROP TABLE IF EXISTS news")
                cur.execute("CREATE TABLE news(ID INT, TITLE TEXT, LINK TEXT, AUTHOR TEXT, DATE TEXT, CONTENT TEXT)")
                i = 0
                for obj in objects:
                    cur.execute("INSERT INTO news VALUES (?, ?, ?, ?, ?, ?)", (i, obj[0], obj[1], obj[2], obj[3], obj[4]))
                    i = i + 1
                messagebox.showinfo(message="BD creada correctamente con " + str(len(objects)) + " respuestas", title="Aviso")
        except lite.Error as e:
            print("Error {}:".format(e.args[0]))
            messagebox.showinfo(message="Se ha producido un error", title="Aviso")
            sys.exit(1)
        finally:
            if con:
                con.close()

    # Obtiene el conjunto de elementos a seleccionar en función de la categoría
    def spin_box_aux(self, category):
        res = []
        if category == 'author':
            aux = self.find.find_db('', 'author_elements')
            for e in aux:
                if e not in res:
                    res.append(e)
        if category == 'date':
            aux = self.find.find_db('', 'dates_elements')
            for e in aux:
                if e[0] not in res:
                    res.append(e[0])
        res.sort()
        return res

    # Crea una spin box con los elementos de la categoria dada
    # Para que funcoine hay que añadir en spin_box_aux y en find_db los correspondientes if y elseif para ajustar la configuración
    def spin_box(self, category):

        # Búsqueda final de elemnto, cogemos el elemento seleccionado por el usuario
        def search():
            res = self.find.find_db(lb.get(), category)
            self.print_with_scroll(res)

        elements = self.spin_box_aux(category)
        if len(elements) > 0:
            master = Tk()
            lb = Spinbox(master, values=elements, width=10)
            lb.pack()
            button = Button(master, text='Buscar', command=search)
            button.pack(side=LEFT)
            master.mainloop()
        else:
            messagebox.showinfo(message='No hay elementos suficientes para realizar la búsqueda', title="Aviso")

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
        find_menu.add_command(label="Por nombre de autor", command=lambda: self.spin_box('author'))
        find_menu.add_command(label="Por fecha", command=lambda: self.search_box('date'))

        root.mainloop()


if __name__ == "__main__":
    Window().start()
