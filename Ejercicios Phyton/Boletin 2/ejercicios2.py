import urllib
from urllib import request
from urllib.request import re
from urllib.error import HTTPError
import dateutil.parser


if __name__ == "__main__":
    try:
        f = request.urlopen('http://www.us.es/rss/feed/portada')
        tag = f.read().decode(f.headers.get_content_charset())
        titulos = re.findall('<title>([^<]*)</title>', tag)
        links = re.findall('<link>([^<]*)</link>', tag)
        fechas = re.findall('<pubDate>([^<]*)</pubDate>', tag)

        i = 1
        while i < len(titulos):
            print('Título: ', titulos[i])
            print('Link: ', links[i])
            print('Fecha: ', dateutil.parser.parse(fechas[i]).strftime("%d/%m/%Y"), '\n')
            i = i + 1

        f.close()
    except HTTPError as e:
        print("Ocurrió un error")
        print(e.code)
    except HTTPError as e:
        print('Ocurrió un error')
        print(e.reason)



