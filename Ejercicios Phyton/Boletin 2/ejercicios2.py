import urllib
from urllib import request
from urllib.request import re
from urllib.error import HTTPError
import dateutil.parser


def capturar(url):
    f = request.urlopen(url)
    captura = f.read().decode(f.headers.get_content_charset())
    f.close()
    return captura


def filtra(filtro, captura):
    return re.findall(filtro, captura)


def imprime(captura_filtrada):
    for elemento in captura_filtrada:
        print('Título: ', elemento[0])
        print('Link: ', elemento[1])
        print('Fecha: ', dateutil.parser.parse(elemento[3]).strftime("%d/%m/%Y"), '\n')


if __name__ == "__main__":
    try:
        aux = []
        mes = input('Introduzca un mes de búsqueda(00, 01, ...):\n')
        tag = capturar('http://www.us.es/rss/feed/portada')
        captura_filtrada = filtra(r'<item>\s*<title>(.*)</title>\s*<link>(.*)</link>\s*<description>.*</description>\s*<author>.*</author>\s*(<category>.*</category>)?\s*<guid.*</guid>\s*<pubDate>(.*)</pubDate>\s*</item>', tag)
        for i in range(len(captura_filtrada)):
            fecha = dateutil.parser.parse(captura_filtrada[i][3]).strftime("%d/%m/%Y")
            if mes in fecha:
                aux.append(captura_filtrada[i])
        if len(aux) > 0: imprime(aux)
    except HTTPError as e:
        print("Ocurrió un error")
        print(e.code)
    except HTTPError as e:
        print('Ocurrió un error')
        print(e.reason)



