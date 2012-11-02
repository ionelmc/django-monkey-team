import sys
import os

from Crypto.Cipher import AES

from django.views.debug import technical_500_response

from .admin import MonkeySetup

RESPONSE_BODY = (
    '<html><!-- %(client_key)s --><head>'
        '<meta http-equiv="content-type" content="text/html; charset=UTF-8">'
        '<title>500 Internal Server Error</title>'
    '</head>'
    '<body>'
    '<h1>500 Internal Server Error</h1>'
    '<p>Sorry, something went wrong.<br><br>A team of highly trained monkeys has been dispatched to deal with this situation.</p>'
    'If you see them, show them this information:<br>'
    '<pre>%(data)s</pre>'
    '<script>%(extra)s</script>'
    '</body></html>'
)
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s : s[0:-ord(s[-1])]

class MonkeyTeamMiddleware(object):

    @staticmethod
    def patch_response(request, response):
        iv = os.urandom(16)
        response.content = RESPONSE_BODY % {
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
        }

    def process_exception(self, request, exception):
        exc_info = sys.exc_info()
        if exc_info:
            response = technical_500_response(request, *exc_info)
        else:
            response = technical_500_response(request, type(exception), exception, None)
        self.patch_response(request, response)
        return response