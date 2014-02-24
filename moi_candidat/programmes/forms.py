from django import forms


class PreThematiqueForm(forms.Form):
    sous_thematiques = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)


class ThematiqueForm(forms.Form):
    proposition = forms.CharField(widget=forms.HiddenInput)
