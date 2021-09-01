from django import forms

class InputForm(forms.Form):
    # HeLO score of team 1
    HeLO_Score_Team1 = forms.CharField(max_length=5)
    # HeLO score of team 2
    h2 = forms.CharField(max_length=5)
    score = forms.CharField(max_length=3)
