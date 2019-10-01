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
        cadena = input();
        res = ""
        i = 0;
        while i < len(cadena) - 1:
            if
            res = res + cadena[i] + cadena
            i = i + 1

if __name__ == '__main__':
    cadena = cadena()
#   EJERCICIO 1 CADENA DE CARACTERES
#    cadena.e1_a()
#    cadena.e1_b()
#    cadena.e1_c()

#   EJERCICIO 2 TUPLAS Y LISTAS



