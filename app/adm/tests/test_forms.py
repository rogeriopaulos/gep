from adm.forms import AdministrativoForm, AdministrativoUpdateForm
from adm.tests.factories import AdministrativoFactory
from core.tests.factories import AssuntoAdministrativoFactory
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class AdministrativoFormTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.assunto_adm = AssuntoAdministrativoFactory()

    def setUp(self):
        self.processo = AdministrativoFactory.build()
        self.valor_invalido = 'NaN'
        self.full_context = {
            'assunto_adm': self.assunto_adm.pk,
            'destino_adm': self.processo.destino_adm,
            'oficiante': self.processo.oficiante,
            'outro': self.processo.outro,
            'email': self.processo.email,
            'fone': self.processo.fone,
            'observacao': self.processo.observacao,
        }
        self.arquivo = {'arquivo': SimpleUploadedFile('arquivo.pdf', b'arquivo')}

    def test_adm_form_invalido_metodo_clean(self):

        assunto_adm_outros = AssuntoAdministrativoFactory(assunto='OUTRO(S)')
        self.full_context['outro'] = ''
        self.full_context['assunto_adm'] = assunto_adm_outros.pk
        form = AdministrativoForm(self.full_context, files=self.arquivo, instance=assunto_adm_outros)
        form.is_valid()

        with self.assertRaisesMessage(ValidationError, "O campo 'Outro(s)' deve ser preenchido"):
            form.clean()


class AdministrativoUpdateFormTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.assunto_adm = AssuntoAdministrativoFactory()
        AdministrativoFactory()

    def setUp(self):
        self.processo = AdministrativoFactory.build()
        self.valor_invalido = 'NaN'
        self.full_context = {
            'assunto_adm': self.assunto_adm.pk,
            'destino_adm': self.processo.destino_adm,
            'oficiante': self.processo.oficiante,
            'outro': self.processo.outro,
            'email': self.processo.email,
            'fone': self.processo.fone,
            'observacao': self.processo.observacao,
        }
        self.arquivo = {'arquivo': SimpleUploadedFile('arquivo.pdf', b'arquivo')}

    def test_adm_form_invalido_metodo_clean(self):

        assunto_adm_outros = AssuntoAdministrativoFactory(assunto='OUTRO(S)')
        self.full_context['outro'] = ''
        self.full_context['assunto_adm'] = assunto_adm_outros.pk
        form = AdministrativoUpdateForm(
            self.full_context, files=self.arquivo, instance=assunto_adm_outros)
        form.is_valid()

        with self.assertRaisesMessage(ValidationError, "O campo 'Outro(s)' deve ser preenchido"):
            form.clean()
