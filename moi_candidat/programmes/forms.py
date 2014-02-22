from django import forms


class ThematiqueForm(forms.Form):
    proposition = forms.CharField(widget=forms.HiddenInput)
