from django import forms


class YearForm(forms.Form):
    year = forms.IntegerField()

class UserForm(forms.Form):
    user_id = forms.IntegerField()

class CatForm(forms.Form):
    categorias = forms.CharField()
