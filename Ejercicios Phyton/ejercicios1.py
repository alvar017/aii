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

if __name__ == '__main__':
    cadena = cadena()
#    cadena.e1_a()
#    cadena.e1_b()




