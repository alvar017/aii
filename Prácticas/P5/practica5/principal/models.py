from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models


class Occupation(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class User(models.Model):
    id_user = models.TextField(primary_key=True)
    age = models.IntegerField()
    sex_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(choices=sex_choices, max_length=1)
    occupation = models.ForeignKey(Occupation, on_delete=models.SET_NULL, null=True)
    postal_code = models.CharField(max_length=8)

    def __str__(self):
        return 'id_user: ' + self.id_user


class Category(models.Model):
    id_category = models.TextField(primary_key=True)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Film(models.Model):
    id_film = models.TextField(primary_key=True)
    title = models.CharField(max_length=60)
    release_date = models.DateField(null=True)
    imdb_url = models.URLField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


class Punctuation(models.Model):
    PUNCTUATIONS = ((1, 'Muy mala'), (2, 'Mala'), (3, 'Regular'), (4, 'Buena'), (5, 'Muy Buena'))
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id_film = models.ForeignKey(Film, on_delete=models.CASCADE, null=True)
    punctuation = models.IntegerField(verbose_name='Puntuación', validators=[MinValueValidator(0), MaxValueValidator(5)],
                                      choices=PUNCTUATIONS)

    class Meta:
        ordering = ('id_film', 'id_user', )

    def __str__(self):
        return str(self.puntuacion)
