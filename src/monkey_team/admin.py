import hashlib
import os

from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.utils.functional import update_wrapper
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib import admin

USERSCRIPT_CODE = r"""

// ==UserScript==
// @name        MonkeyTeam error response decode script for %(site_name)s
// @include     http*
// @grant       none
// ==/UserScript==

var CLIENT_KEY = "%(client_key)s";
var DECODE_KEY = "%(decode_key)s";

if (document.documentElement.outerHTML.indexOf(CLIENT_KEY) > 0) {
    %(lib_code)s;

    var pre = document.body.getElementsByTagName('pre')[0];
    var data = CryptoJS.enc.Base64.parse(pre.textContent);
    var output = CryptoJS.AES.decrypt(
        CryptoJS.enc.Base64.stringify(CryptoJS.lib.WordArray.create(data.words.slice(4))),
        CryptoJS.enc.Hex.parse(DECODE_KEY),
        {iv: CryptoJS.lib.WordArray.create(data.words.slice(0, 4))}
    ).toString(CryptoJS.enc.Latin1)
    var anchor;
    document.body.appendChild(anchor=document.createElement("a"))
    anchor.setAttribute("href", "#")
    anchor.appendChild(pre)
    anchor.addEventListener("click", function(event){
        event.preventDefault();
        event.stopPropagation();
        console.log(output);
        document.write(output);
    });
    delete data;
    delete pre;
    delete anchor;
}
"""

class TestException(Exception): pass

class Setup(object):
    class _meta:
        abstract = False
        app_label = "monkey_team"
        module_name = "setup"
        verbose_name_plural = "Setup"
        verbose_name = "Setup"
        swapped = False

class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

class MonkeySetup(admin.ModelAdmin):
    has_add_permission = lambda *args: False
    has_change_permission = lambda *args: True
    has_delete_permission = lambda *args: False

    def get_urls(self):

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
            url(r'^$', wrap(self.setup_view), name='%s_%s_changelist' % info),
            url(r'^monkey-team.user.js$',
                wrap(self.userscript_view), name='monkey_team_userscript'),
            url(r'^test/$',
                wrap(self.test_view), name='monkey_team_test'),
        )
        return urlpatterns

    @classproperty
    def client_key(cls):
        return hashlib.sha1(
            "monkey-team-match-id-%s" % settings.SECRET_KEY
        ).hexdigest()

    @classproperty
    def decode_key(cls):
        return hashlib.sha256(
            "monkey-team-decode-key-%s" % settings.SECRET_KEY
        ).digest()

    def test_view(self, request):
        raise TestException("Relax, it's just a test ...")

    def userscript_view(self, request):
        response = HttpResponse(
            self.get_userscript_code(request),
            mimetype='application/javascript'
        )
        response['Content-Disposition'] = 'attachment; filename="monkey-team-%s.user.js"' % self.client_key
        return response

    @classmethod
    def get_userscript_code(cls, request):
        return USERSCRIPT_CODE % {
            'client_key': cls.client_key,
            'decode_key': cls.decode_key.encode('hex').strip(),
            'lib_code': file(os.path.join(os.path.dirname(__file__), 'aes.js')).read(),
            'site_name': request.get_host(),
        }

    def setup_view(self, request):
        return render(request, "monkey_setup.html", {
            'userscript_url': reverse('admin:monkey_team_userscript'),
            'test_url': reverse('admin:monkey_team_test'),
            'warn_middleware': 'monkey_team.middleware.MonkeyTeamMiddleware' not in settings.MIDDLEWARE_CLASSES,
            'warn_debug': settings.DEBUG,
        })

admin.site.register((Setup,), MonkeySetup)