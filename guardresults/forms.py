from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(min_length=1)
    tag = forms.CharField()
    section = forms.CharField()
    page_size = forms.IntField()
    date_id = forms.Charfield()
    
