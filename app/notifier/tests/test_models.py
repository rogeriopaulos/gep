from django.test import TestCase

from .factories import TelegramUserFactory


class TelegramUserTestCase(TestCase):

    def setUp(cls):
        cls.telegram = TelegramUserFactory()

    def test_str(self):
        resultado_esperado = self.telegram.user.__str__()
        self.assertEqual(str(self.telegram), resultado_esperado)

    def test_get_absolute_url(self):
        resultado_esperado = '/notificacao/habilitar-telegram/'
        self.assertEqual(self.telegram.get_absolute_url(), resultado_esperado)

    def test_get_tipo_procedimento(self):
        resultado_esperado = 'Cadastro Telegram'
        self.assertEqual(self.telegram.get_tipo_procedimento(), resultado_esperado)
