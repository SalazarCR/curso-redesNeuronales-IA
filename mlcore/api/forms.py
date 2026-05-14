from django import forms

class DataForm(forms.Form):
    feature1 = forms.FloatField()
    feature2 = forms.FloatField()
    feature3 = forms.FloatField()