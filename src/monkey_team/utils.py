import hashlib
import os
from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string

def get_client_key():
    return hashlib.sha1(
        "monkey-team-match-id-%s" % settings.SECRET_KEY
    ).hexdigest()

def get_decode_key():
    return hashlib.sha256(
        "monkey-team-decode-key-%s" % settings.SECRET_KEY
    ).digest()

def get_decode_key_hex():
    return get_decode_key().encode('hex').strip()

def get_userscript_code(request):
    return render_to_string("monkey-team.user.js", {
        'client_key': get_client_key(),
        'decode_key': get_decode_key_hex(),
        'lib_code': file(os.path.join(os.path.dirname(__file__), 'aes.js')).read(),
        'site_name': request.get_host(),
    }, context_instance=RequestContext(request))
