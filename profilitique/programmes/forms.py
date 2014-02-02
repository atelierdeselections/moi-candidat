from django import forms


class Thematique1(forms.Form):
    thematique = forms.IntegerField()
    proposition = forms.IntegerField()


class Thematique2(forms.Form):
    thematique = forms.IntegerField()
    proposition = forms.IntegerField()
