from django.db import models


class Lenguaje(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return "{0}".format(self.nombre)


class Municipio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return "{0}".format(self.nombre)


class Tipoevento(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return "{0}".format(self.nombre)


class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_evento = models.ForeignKey(Tipoevento, on_delete=models.SET_NULL,null=True)
    fecha_inicio_evento = models.DateField(null=True)
    lenguajes = models.ManyToManyField(Lenguaje)
    nombre_lugar = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True)
    pais = models.CharField(max_length=100)

    def __str__(self):
        return "{0}".format(self.nombre)


