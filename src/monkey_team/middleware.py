import sys
import os

from Crypto.Cipher import AES

from django.views.debug import technical_500_response
from django.template.loader import render_to_string

from .admin import MonkeySetup

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s : s[0:-ord(s[-1])]

class MonkeyTeamMiddleware(object):

    @staticmethod
    def patch_response(request, response):
        iv = os.urandom(16)
        response.content = render_to_string("monkey_500.html", {
            'client_key': MonkeySetup.client_key,
            'data': (
                iv + AES.new(
                    MonkeySetup.decode_key,
                    AES.MODE_CBC,
                    iv,
                ).encrypt(
                    pad(response.content)
                )
            ).encode('base64'),
            'extra': ''#MonkeySetup.get_userscript_code(request),
        })

    def process_exception(self, request, exception):
        exc_info = sys.exc_info()
        if exc_info:
            response = technical_500_response(request, *exc_info)
        else:
            response = technical_500_response(request, type(exception), exception, None)
        self.patch_response(request, response)
        return response