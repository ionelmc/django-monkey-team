from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings

from monkey_team.admin import TestException

class MonkeyTeamTestCase(TestCase):
    def setUp(self):
        self.user = User(
            username='test', email='test@example.com', is_active=True,
            is_staff=True, is_superuser=True,
        )
        self.user.set_password('test')
        self.user.save()
        self.client.login(username='test', password='test')

    def test_admin_not_broken(self):
        response = self.client.get('/admin/')
        self.assertContains(response, '/admin/password_change/')
        self.assertNotContains(response, "You don't have permission to edit anything")

    def test_admin_auth_not_broken(self):
        response = self.client.get('/admin/auth/')
        self.assertEqual(response.status_code, 200, response)

    def test_admin_auth_user_not_broken(self):
        response = self.client.get('/admin/auth/user/')
        self.assertEqual(response.status_code, 200, response)

    def test_admin_monkey_setup(self):
        response = self.client.get('/admin/monkey_team/')
        self.assertEqual(response.status_code, 200, response)
        response = self.client.get('/admin/monkey_team/setup/')
        self.assertEqual(response.status_code, 200, response)

    def test_admin_monkey_test(self):
        response = self.client.get('/admin/monkey_team/setup/test/')
        self.assertContains(response, "A team of highly trained monkeys has been dispatched to deal with this situation.", status_code=500)

    def test_admin_monkey_test_debug(self):
        settings.DEBUG = True
        self.assertRaises(TestException, self.client.get, '/admin/monkey_team/setup/test/')
        settings.DEBUG = False

    def test_admin_monkey_setup_debug(self):
        settings.DEBUG = True
        response = self.client.get('/admin/monkey_team/setup/')
        self.assertContains(response, "Highly trained monkeys do not have")
        settings.DEBUG = False

    def test_admin_userscript_generate(self):
        response = self.client.get('/admin/monkey_team/setup/monkey-team.user.js')
        self.assertContains(response, "CLIENT_KEY")
        self.assertContains(response, "var CryptoJS=CryptoJS")
