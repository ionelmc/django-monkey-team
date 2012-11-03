import hashlib
import os
from django.conf import settings
from django.template import RequestContext
from django.conf.urls.defaults import patterns
from django.utils.functional import update_wrapper
from django.template.loader import render_to_string
from django.contrib import admin

__all__ = 'make_admin_class',

def make_admin_class(name, urls, app_label="monkey_team", dont_register=False):

    class _meta:
        abstract = False
        app_label = "monkey_team"
        module_name = name.lower()
        verbose_name_plural = name
        verbose_name = name
        swapped = False
    model_class = type(name, (object,), {'_meta': _meta})

    class admin_class(admin.ModelAdmin):
        has_add_permission = lambda *args: False
        has_change_permission = lambda *args: True
        has_delete_permission = lambda *args: False

        def get_urls(self):
            def wrap(view):
                def wrapper(*args, **kwargs):
                    return self.admin_site.admin_view(view)(*args, **kwargs)
                return update_wrapper(wrapper, view)
            from django.core.urlresolvers import RegexURLPattern
            return [ # they are already prefixed
                RegexURLPattern(
                    str(url.regex.pattern),
                    wrap(url.callback),
                    url.default_args,
                    url.name
                ) if isinstance(url, RegexURLPattern)
                  else url
                for url in urls
            ]

        @classmethod
        def register(cls):
            admin.site.register((model_class,), cls)
    if not dont_register:
        admin_class.register()
    return admin_class

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
