import tkinter as tk
from tkinter import *
from urllib import request
from tkinter import messagebox, Tk
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
        products = soup.findAll("div", {"class": "grid__item m-one-whole t-one-third d-one-third dw-one-quarter | js-product-grid-grid"})
        for i in range(len(products)):
            brand = products[i].find("h4", {"class": "product-item__brand micro | push-half--bottom"}).find("a").text.strip()
            name = products[i].find("h3", {"class": "product-item__name zeta face-normal | flush--bottom"}).find("a").get("title")[8:]
            link = "https://www.ulabox.com/" + products[i].find("h3", {"class": "product-item__name zeta face-normal | flush--bottom"}).find("a").get("href")
            price_discoun = products[i].find("article").get("data-price")
            price_normal = products[i].find("span", {"class": "product-grid-footer__price"})
            price_normal_aux = products[i].find("span", {"class": "product-grid-footer__price"})
            price_normal = price_normal_aux.find("del", {
                "class": "product-item__price product-item__price--old product-grid-footer__price--old nano | flush--bottom"})
            if price_normal is None:
                price_normal = price_discoun
            else:
                price_normal = price_normal.text
                price_normal = str(price_normal)[:-2]

            aux = [brand, name, link, price_normal, price_discoun]
            res.append(aux)
        return res

    def print_with_scroll(self, threads):
        res = []
        # aux = [brand, name, link, price_normal, price_discoun]
        for thread in threads:
            aux = ['Nombre: ' + thread[2] + '\n', 'Precio final: : ' + thread[5]]
            res.append(aux)

        v = Toplevel()
        sc = Scrollbar(v)
        sc.pack(side=RIGHT, fill=Y)
        lb = Listbox(v, width=150, yscrollcommand=sc.set)
        for row in res:
            lb.insert(END, row[0])
            lb.insert(END, row[1])
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
        c = self.find.find_url('https://www.ulabox.com/campaign/productos-sin-gluten#gref')
        con = None
        try:
            con = lite.connect('test.db')
            with con:
                cur = con.cursor()
                cur.execute("DROP TABLE IF EXISTS products")
                cur.execute("CREATE TABLE products(ID INT, BRAND TEXT, NAME TEXT, LINK TEXT, PRICE_NORMAL TEXT, PRICE_DISCOUN TEXT)")
                for i in range(len(c)):
                    cur.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)", (i, c[i][0], c[i][1], c[i][2], c[i][3], c[i][4]))
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
        root.resizable(0, 0)

        # Esta referencia debe mantenerse mientra necesitemos el fondo
        background_image = tk.PhotoImage(file=r"./us.png")

        w = background_image.width()
        h = background_image.height()

        root.geometry("{}x{}+{}+{}".format(w, h, 0, 0))

        background_label = tk.Label(root, image=background_image)
        background_label.pack(side='top', fill='both', expand='yes')

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

        find_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Buscar", menu=find_menu)
        find_menu.add_command(label="Tema", command=window.find_title)
        find_menu.add_command(label="Fecha", command=window.find_date)

        estadistics_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Estadísticas", menu=estadistics_menu)
        estadistics_menu.add_command(label="Temas más populares", command=find.find_more_popular)
        estadistics_menu.add_command(label="Temas más activos", command=find.find_more_active)

        root.mainloop()


if __name__ == "__main__":
    Window().start()
