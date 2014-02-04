from django import forms


class ThematiqueForm(forms.Form):
    proposition = forms.IntegerField(widget=forms.HiddenInput)
