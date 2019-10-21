class Cadena:
    # Ejercicio 1. Escribir funciones que dada una cadena y un caracter:

    # a) Inserte el caracter entre cada letra de la cadena.
    #       Ej: ’separar’ y ’,’ debería devolver ’s,e,p,a,r,a,r’
    def e1_a(self):
        print("Inserte cadena \n")
        palabra = input();
        print("Inserte caracter \n")
        elemento = input()
#        res = ""
#        i = 0;
#        while i < len(palabra) - 1:
#            res = res + palabra[i] + elemento
#            i = i + 1
#        res = res + palabra[i]
        res = elemento.join(list(palabra))
        print("Su solución: " + res)
        return res

#    b) Reemplace todos los espacios por el caracter.Ej: ’mi archivo de texto.txt’ y ’_’ debería
#       devolver ’mi_archivo_de_texto.txt’
    def e1_b(self):
        print("Inserte cadena \n")
        cadena = input();
        res = cadena.replace(" ", "_")
        print("Su solución: " + res)
        return res

#   c) Reemplace todos los dígitos en la cadena por el caracter. Ej: ’su clave es: 1540’ y ’X’ debería
#      devolver ’su clave es: XXXX’
    def e1_c(self):
        translation_table = str.maketrans('0123456789', 'XXXXXXXXXX')
        print("Inserte cadena \n")
        cadena = input();
        res = cadena.translate(translation_table)
        print(res)
        return res

#   d) Inserte el caracter cada 3 dígitos en la cadena. Ej. ’2552552550’ y ’.’ debería devolver ’255.255.255.0’
    def e1_d(self):
        print("Inserte cadena \n")
        cadena = input()
        res = ""
        i = 0
        while i < len(cadena):
            res = res + cadena[i]
            if (i+1) % 3 == 0 and i != 0:
                res = res + "."
            i = i + 1
        print("Su solución es: " + res)
        return res


class Lista:
#   Ejercicio 1. Campaña electoral

#   a) Escribir una función que reciba una tupla con nombres, y para cada nombre imprima el mensaje Estimado
#      < nombre >, vote por mí.
    def e2_a(self, tupla):
        for e in tupla:
            print("Estimado/a", e, ", vote por mí.")

#   b) Escribir una función que reciba una tupla con nombres, una posición de origen py una
#      cantidad n, e imprima el mensaje anterior para los n nombres que se encuentran a partir de la
#      posición p.
    def e2_b(self, tupla, posicion_o, cantidad):
#        i = 1
#        for e in tupla:
#            if posicion_o <= tupla.index(e) and i <= cantidad:
#                print(e)
#                i = i + 1
        t1 = tupla[posicion_o:posicion_o + cantidad]
        self.e2_a(t1)

#   c) Modificar las funciones anteriores para que tengan en cuenta el género del destinatario,
#      para ello, deberán recibir una tupla de tuplas, conteniendo el nombre y el género.
    def e2_c(self, tupla):
        for e in tupla:
            print("Estimado " if e[1] == "h" else "Estimada ", e[0], ", vote por mí.")

#   Ejercicio 2.
#       Escribir una función que reciba una lista de tuplas (Apellido, Nombre, Inicial, segundo_nombre)
#       y devuelva una lista de cadenas donde cada una contenga primero el nombre, luego la inicial con
#       un punto, y luego el apellido.
    def e2_a_bis(self, tuplas):
        for e in tuplas:
            print(e[1], e[3], e[2] + ".", e[0])


class Busqueda:
#   Ejercicio 1. Agenda simplificada
#       Escribir una función que reciba una cadena a buscar y una lista de tuplas (nombre_completo,
#       telefono), y busque dentro de la lista, todas las entradas que contengan en el nombre
#       completo la cadena recibida (puede ser el nombre, el apellido o sólo una parte de cualquiera
#       de ellos). Debe devolver una lista con todas las tuplas encontradas.

    def e1(self, cadena, tuplas):
        for t in tuplas:
            if cadena in t[0]:
                print('Nombre:', t[0] + ', teléfono:', t[1])


class Diccionario:
#   Ejercicio 1. Continuación de la agenda.
#       Escribir un programa que vaya solicitando al usuario que ingrese nombres.
#           a) Si el nombre se encuentra en la agenda (implementada con un diccionario), debe mostrar el teléfono y, opcionalmente,
#              permitir modificarlo si no es correcto.
#           b) Si el nombre no se encuentra, debe permitir ingresar el teléfono correspondiente.
#       El usuario puede utilizar la cadena "*", para salir del programa.
    def e1(self, diccionario):
        while True:
            print("Introduzca nombre: ")
            cadena = input()
            if cadena == '*':
                break
            if cadena in diccionario:
                print('Teléfono: ', diccionario[cadena])
                respuesta = input('¿Es correcto (s/n)')
                if respuesta == 'n':
                    numero = input('Introduzca nuevo número: ')
                    diccionario[cadena] = numero
            else:
                numero = input('Introduzca un número para '+ cadena + ": ")
                diccionario[cadena] = numero


#    Ejercicio 1. Botella y Sacacorchos
#       a) Escribir una clase Corcho, que contenga un atributo bodega(cadena con el nombre de la bodega).
class Corcho:
    def __init__(self, nombre):
        self.bodega = nombre


#       b) Escribir una clase Botella que contenga un atributo corcho con una referencia al corcho que la tapa, o None
#          si está destapada.
class Botella:
    def __init__(self, corcho):
        self.corcho = corcho


#       c) Escribir una clase Sacacorchos que tenga un método destapar que le reciba una botella, le saque el corcho y
#          se guarde una referencia al corcho sacado.
#       d) Agregar un método limpiar, que saque el corcho del sacacorchos.
class Sacacorchos:
    def __init__(self):
        self.corcho = None

    def c(self, botella):
        print("Descorchar")
        self.corcho = botella.corcho
        botella.corcho = None

    def d(self, sacacorchos):
        sacacorchos.corcho = None


#   Herencia y polimorfirmos
#       Ejercicio 1. Juego de Rol
#           a) Escribir una clase Personaje que contenga los atributos vida, posicion y velocidad, y los
#              métodos recibir_ataque, que reduzca la vida según una cantidad recibida y lance un mensaje si
#              la vida pasa a ser menor o igual que cero, y mover que reciba una dirección y se mueva en esa
#              dirección la cantidad indicada por velocidad.
class Personaje:
    def __init__(self, vida, posicion, velocidad):
        self.vida = vida
        self.posicion = posicion
        self.velocidad = velocidad

    def recibir_ataque(self, cantidad):
        self.vida = self.vida - cantidad
        if self.vida <= 0:
            print("WASTED")
        else:
            print('Te queda', self.vida, 'vida')

    def mover(self, direccion):
        self.posicion[direccion] = self.posicion[direccion] + self.velocidad
        print('Su nueva posición es:', self.posicion)


#           b) Escribir una clase Soldado que herede de Personaje, y agregue el atributo ataque y el
#              método atacar, que reciba otro personaje, al que le debe hacer el daño indicado por el
#              atributo ataque.
class Soldado(Personaje):
    def __init__(self, personaje, ataque):
        self.personaje = personaje
        self.ataque = ataque

    def atacar(self, soldado):
        soldado.personaje.vida = soldado.personaje.recibir_ataque(self.ataque)


#           c) Escribir una clase Campesino que herede de Personaje, y agregue el atributo cosecha y el
#              método cosechar, que devuelva la cantidad cosechada.
class Campesino(Personaje):
    def __init__(self, personaje, cosecha):
        self.personaje = personaje
        self.cosecha = cosecha

    def cosechar(self):
        print('La cosecha es de:', self.cosecha)
        return self.cosecha

if __name__ == '__main__':
    cadena = Cadena()
#   EJERCICIO 1 CADENA DE CARACTERES
#    cadena.e1_a()
#    cadena.e1_b()
#    cadena.e1_c()
#    cadena.e1_d()

#   EJERCICIO 2 TUPLAS Y LISTAS
    lista = Lista()
#    lista.e2_a(('Luis', 'Marta', 'Paula'))
#    lista.e2_b(('Luis', 'Marta', 'Paula'), 1, 2)
#    lista.e2_c((('Luis', 'h'), ('Marta', 'm'), ('Paula', 'm')))
#    lista.e2_a_bis((('de la Flor Bonilla', 'Álvaro', 'Á', 'Pilo'), ('de la Flor Bonilla', 'Carlos', 'CJ', 'Javier'), ('de la Flor Bonilla', 'Patricia', 'P', 'Lucía')))

#   EJERCICIO 3 BÚSQUEDA
    busqueda = Busqueda()
#    busqueda.e1('García', (('Jorge García', '12345'), ('Luisa Montero', '54321'), ('Inés Roca Díaz', '67890')))

#   EJERCICIO 4 DICCIONARIO
    diccionario = Diccionario()
#    diccionario.e1(({'Jorge': '12345', 'Luisa': '54321', 'Marta': '67890'}))

#   EJERCICIO 5 OBJETOS
    # Creo un corcho
#    corcho = Corcho('Bodega de la Flor')
#    print(corcho.bodega)

    # Creo una botella y le asigno el corcho anterior
#    botella = Botella(corcho)
#    print(botella.corcho.bodega)

    # Creo un sacacorchos y compruebo que no tiene ningún corcho actualmente
#    sacacorchos = Sacacorchos()
#    print('Corcho: ', sacacorchos.corcho)

    # Descorcho la botella (compruebo que la botella se queda descorchada) y compruebo que el corcho se queda en el sacacorchos
#    sacacorchos.c(botella)
#    print('Corcho después de descorchar:', botella.corcho)
#    print('Corcho en sacacorchos antes de limpiar:', sacacorchos.corcho.bodega)

    # Limpio el sacacorchos y compruebo que se queda vacío
#    sacacorchos.d(sacacorchos)
#    print('Corcho en sacacorchos después de limpiar:', sacacorchos.corcho)

#   EJERCICIO 6 HERENCIA Y POLIMORFISMO
#       Apartado a)
#    personaje1 = Personaje(100, {"Norte": 0, "Sur": 0, "Este": 0, "Oeste": 0}, 10)
#    personaje2 = Personaje(100, {"Norte": 0, "Sur": 0, "Este": 0, "Oeste": 0}, 10)
#    personaje1.recibir_ataque(5)
#    personaje2.recibir_ataque(101)

#    personaje1.mover('Norte')
#    personaje1.mover('Norte')
#    personaje1.mover('Oeste')

#       Apartado b)
#    personaje_atacado = Personaje(100, {"Norte": 0, "Sur": 0, "Este": 0, "Oeste": 0}, 10)
#    personaje_atacante = Personaje(100, {"Norte": 0, "Sur": 0, "Este": 0, "Oeste": 0}, 10)

#    soldado_atacado = Soldado(personaje_atacado, 50)
#    soldado_atacante = Soldado(personaje_atacante, 50)

#    print('Ataque 1')
#    soldado_atacante.atacar(soldado_atacado)
#    print('Ataque 2')
#    soldado_atacante.atacar(soldado_atacado)

#       Apartado c)
#    personaje = Personaje(100, {"Norte": 0, "Sur": 0, "Este": 0, "Oeste": 0}, 10)
#    personaje_campesino = Campesino(personaje, 100)
#    personaje_campesino.cosechar()







