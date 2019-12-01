# encoding:utf-8
from django import forms


class UserSearchForm(forms.Form):
    user_id = forms.CharField(label="Id de Usuario", widget=forms.TextInput, required=True)


class FilmSearchByYearForm(forms.Form):
    year = forms.IntegerField(label="Año de publicación", widget=forms.TextInput, required=True)
