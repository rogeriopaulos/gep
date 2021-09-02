from account.forms import UserEditForm, UserForm
from account.tests.factories import UserFactory
from django.test import TestCase


class UserFormTestCase(TestCase):

    def setUp(self):
        self.usr = UserFactory()

        self.data = {
            'username': self.usr.username,
            'first_name': self.usr.first_name,
            'last_name': self.usr.last_name,

            'email': self.usr.email,
            'password': self.usr.password,
        }

    def test_operacao_repetida(self):
        email_indisponivel_error_message = 'Já existe um usuário com este e-mail.'
        form = UserForm(data=self.data)
        self.assertFalse(form.is_valid())
        form.clean()
        self.assertIn(('email', [email_indisponivel_error_message]), form.errors.items())


class UserEditFormTestCase(TestCase):

    def setUp(self):
        self.usr = UserFactory()

        self.data = {
            'username': self.usr.username,
            'first_name': self.usr.first_name,
            'last_name': self.usr.last_name,

            'email': self.usr.email,
            'password': self.usr.password,
        }

    def test_operacao_repetida(self):
        email_indisponivel_error_message = 'Já existe um usuário com este e-mail.'
        form = UserEditForm(data=self.data)
        self.assertFalse(form.is_valid())
        form.clean()
        self.assertIn(('email', [email_indisponivel_error_message]), form.errors.items())
