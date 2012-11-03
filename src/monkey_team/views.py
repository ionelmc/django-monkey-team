from Crypto.Cipher import AES

from django.conf import settings
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render

from .utils import get_client_key, get_userscript_code, get_decode_key
from .forms import DecodeForm

class TestException(Exception):
    pass

def userscript(request):
    response = HttpResponse(
        get_userscript_code(request),
        mimetype='application/javascript'
    )
    response['Content-Disposition'] = 'attachment; filename="monkey-team-%s.user.js"' % get_client_key()
    return response

def test(_request):
    raise TestException("Relax, it's just a test ...")

def setup(request):
    return render(request, "monkey_setup.html", {
        'userscript_url': reverse('admin:monkey_team_userscript'),
        'test_url': reverse('admin:monkey_team_test'),
        'warn_middleware': 'monkey_team.middleware.MonkeyTeamMiddleware' not in settings.MIDDLEWARE_CLASSES,
        'warn_debug': settings.DEBUG,
    })

def decode(request):
    if request.method == "POST":
        form = DecodeForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            optional_decode_key = form.cleaned_data['optional_decode_key']
            decode_key = optional_decode_key or get_decode_key()
            return HttpResponse(
                AES.new(
                    decode_key,
                    AES.MODE_CBC,
                    message[:16],
                ).decrypt(
                    message[16:]
                )
            )
    else:
        form = DecodeForm()
    return render(request, "monkey_decode.html", {
        "form": form
    })