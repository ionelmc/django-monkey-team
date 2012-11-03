from Crypto.Cipher import AES

from django import forms
from django.forms import ValidationError
from .utils import get_decode_key

class DecodeForm(forms.Form):
    optional_decode_key = forms.CharField(required=False)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_optional_decode_key(self):
        optional_decode_key = self.cleaned_data['optional_decode_key'].strip()
        if optional_decode_key:
            if len(optional_decode_key) != 64:
                raise ValidationError('Invalid length for decode key !')
            try:
                decode_key = optional_decode_key.decode('hex')
            except TypeError as e:
                raise ValidationError('Cannot convert to binary: %r' % e.msg)

            return decode_key

    def clean_message(self):
        message = self.cleaned_data['message']
        try:
            message = message.decode('base64')
        except TypeError as e:
            raise ValidationError('Cannot convert to binary: %r' % e.msg)

        if len(message) % 16:
            raise ValidationError('Wrong block size for message !')

        if len(message) <= 16:
            raise ValidationError('Message too short or missing IV !')

        return message
