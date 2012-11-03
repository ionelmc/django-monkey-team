from django import forms

class DecodeForm(forms.Form):
    optional_decode_key = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea, required=True)