from django.db import models


class Occupation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{0}".format(self.name)


class Category(models.Model):
    category_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{0} - {1}".format(self.id, self.name)


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    age = models.IntegerField()
    choices = [("m", "M"), ("f", "F")]
    sex = models.CharField(max_length=1, choices=choices)
    occupation = models.ForeignKey(Occupation, on_delete=models.SET_NULL, null=True)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return "USER ID:{0}".format(self.user_id)


class Film(models.Model):
    film_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    release_date = models.DateField(null=True)
    url = models.URLField(null=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return "FILM ID:{0}".format(self.film_id)


class Punctuation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    rank = models.IntegerField()

    def __str__(self):
        return "ID: {0} RANK:{1}".format(self.film_id, self.rank)


