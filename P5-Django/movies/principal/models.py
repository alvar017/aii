from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class Ocupacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return "{0}".format(self.nombre)

class Categoria(models.Model):
    id_categoria = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return "{0}".format(self.nombre)


class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True)
    edad = models.IntegerField()
    choices = [("m", "M"), ("f", "F")]
    sexo = models.CharField(max_length=1,choices=choices) 
    ocupacion = models.ForeignKey(Ocupacion, on_delete=models.SET_NULL, null=True)
    codigo_postal = models.CharField(max_length=20)

    def __str__(self):
        return "Id:{0} - Edad:{1} - Código postal:{2}".format(self.id_usuario, self.edad, self.codigo_postal)

class Pelicula(models.Model):
    id_pelicula = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=100)
    fecha_estreno = models.DateField(null=True)
    url = models.CharField(max_length=100, null=True)
    categorias = models.ManyToManyField(Categoria)

    def __str__(self):
        return "Id:{0} - Título:{1}".format(self.id_pelicula, self.titulo)

class Puntuacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    valoracion = models.IntegerField()

    def __str__(self):
        return "Valoración:{0} - Película -->{1} ".format(self.valoracion, self.pelicula)


