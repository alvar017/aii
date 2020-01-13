from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,URLValidator

class Libro(models.Model):
    book_id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    genero = models.CharField(max_length=255)
    idioma = models.CharField(max_length=255)
    rating1 = models.IntegerField()
    rating2 = models.IntegerField()
    rating3 = models.IntegerField()
    rating4 = models.IntegerField()
    rating5 = models.IntegerField()

    def __str__(self):
        return self.titulo

class Puntuacion(models.Model):
    value = models.IntegerField()
    usuario_id = models.IntegerField()
    book = models.ForeignKey(Libro, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.value 