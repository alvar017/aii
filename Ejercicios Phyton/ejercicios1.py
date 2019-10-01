class cadena:
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

class lista:
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

if __name__ == '__main__':
    cadena = cadena()
#   EJERCICIO 1 CADENA DE CARACTERES
#    cadena.e1_a()
#    cadena.e1_b()
#    cadena.e1_c()
#    cadena.e1_d()

#   EJERCICIO 2 TUPLAS Y LISTAS
    lista = lista()
#    lista.e2_a(('Luis', 'Marta', 'Paula'))
#    lista.e2_b(('Luis', 'Marta', 'Paula'), 1, 2)
#    lista.e2_c((('Luis', 'h'), ('Marta', 'm'), ('Paula', 'm')))




