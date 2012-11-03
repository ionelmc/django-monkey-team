from django.conf.urls.defaults import patterns, url
from .utils import make_admin_class

make_admin_class("Setup", patterns("monkey_team.views",
    url(r'^$', 'setup', name='monkey_team_setup_changelist'),
    url(r'^monkey-team.user.js$', 'userscript', name='monkey_team_userscript'),
    url(r'^decode/$', 'decode', name='monkey_team_test'),
    url(r'^test/$', 'test', name='monkey_team_test'),
))

make_admin_class("Decode", patterns("monkey_team.views",
    url(r'^$', 'decode', name='monkey_team_decode_changelist'),
))






