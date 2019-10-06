import urllib
from urllib import request
from urllib.error import HTTPError


if __name__ == "__main__":
    try:
        f = request.urlopen('http://www.us.es/rss/feed/portada')
        print(f.read())
        f.close()
    except HTTPError as e:
        print("Ocurrió un error")
        print(e.code)
    except HTTPError as e:
        print('Ocurrió un error')
        print(e.reason)



