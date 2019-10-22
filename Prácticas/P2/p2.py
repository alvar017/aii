import tkinter as tk
from tkinter import *
from urllib import request
from bs4 import BeautifulSoup
from tkinter import messagebox, Tk
import sqlite3 as lite
import sys


class Find:
    def find_url(self, url):
        res = []
        f = request.urlopen(url)
        page = f.read().decode(f.headers.get_content_charset())
        f.close()

        soup = BeautifulSoup(page, 'html.parser')
        products = soup\
            .findAll("div", {"class": "grid__item m-one-whole t-one-third d-one-third dw-one-quarter | js-product-grid-grid"})
        for i in range(len(products)):
            brand = products[i].find("h4", {"class": "product-item__brand micro | push-half--bottom"}).find("a").text.strip()
            name = products[i].find("h3", {"class": "product-item__name zeta face-normal | flush--bottom"}).find("a").get("title")[8:]
            link = "https://www.ulabox.com/" + products[i].find("h3", {"class": "product-item__name zeta face-normal | flush--bottom"}).find("a").get("href")
            price_discoun = products[i].find("article").get("data-price")
            price_normal = products[i]\
                .find("span", {
                "class": "product-grid-footer__price"})\
                .find("del", {
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
            if thread[4] != thread[5]:
                aux = ['Nombre: ' + thread[2] + '\n', 'Precio final: ' + thread[5] + '€ (el anterior era : ' + thread[4] + '€)']
            else:
                aux = ['Nombre: ' + thread[2] + '\n', 'Precio final: ' + thread[5] + '€']
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

    def find_db(self, brand):
        conn = lite.connect('test.db')
        conn.text_factory = str
        if brand is not None:
            s = "%" + brand + "%"
            cursor = conn.execute("SELECT * FROM products WHERE BRAND LIKE ?", (s,))
        else:
            cursor = conn.execute("SELECT * FROM products")
        res = []
        for row in cursor:
            res.append(row)
        conn.close()
        return res

    def find_brands(self):
        res = []
        for product in self.find_db(None):
            if product[1] not in res:
                res.append(product[1])
        res.sort()
        return res

    def find_discounts(self):
        res = []
        for product in self.find_db(None):
            if product[4] != product[5]:
                res.append(product)
        res.sort()
        self.print_with_scroll(res)


class Window:
    def __init__(self):
        self.find = Find()

    def find_by_brand(self):
        self.create_spinbox(self.find.find_brands())

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

    def create_spinbox(self, values):
        def finder_aux():
            res = self.find.find_db(lb.get())
            self.find.print_with_scroll(res)
        master = Tk()
        lb = Spinbox(master, values=values, width=10)
        lb.pack()
        button = Button(master, text='Buscar', command=finder_aux)
        button.pack(side=LEFT)
        master.mainloop()

    def start(self):
        window = Window()
        find = Find()

        root = Tk()

        button_save = Button(root, text="Almacenar en la base de datos", command=window.save)
        button_save.pack(side=tk.TOP)
        button_save = Button(root, text="Buscar por marca", command=window.find_by_brand)
        button_save.pack(side=tk.TOP)
        button_find_brand = Button(root, text="Mostrar ofertas", command=find.find_discounts)
        button_find_brand.pack(side=tk.TOP)

        def close_window():
            root.destroy()
        button_find_brand = Button(root, text="Salir", command=close_window)
        button_find_brand.pack(side=tk.LEFT)

        root.mainloop()


if __name__ == "__main__":
    Window().start()
