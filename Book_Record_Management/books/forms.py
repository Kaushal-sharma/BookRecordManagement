from django import forms

class addbookforms(forms.Form):
    title = forms.CharField(label="Title", max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter book name'}))
    author = forms.CharField(label="Author", max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter book author name'}))
    publisher = forms.CharField(label="Publisher", max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter book publisher name'}))
    price = forms.FloatField(label="Price", widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Enter book price'}))
