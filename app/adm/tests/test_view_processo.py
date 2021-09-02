
import json

from adm.tests.factories import AdministrativoFactory
from adm.tests.utils import SetUpTestViewsData
from core.tests.factories import AssuntoAdministrativoFactory
from django.test import Client, TestCase
from django.urls import reverse
from guardian.shortcuts import assign_perm


class AdministrativoCreateViewTestCase(SetUpTestViewsData, TestCase):

    def setUp(cls):
        cls.processo = AdministrativoFactory.build(autor=cls.superior)
        cls.assunto_adm = AssuntoAdministrativoFactory()
        cls.url = reverse('adm:criar_processo_adm')

        cls.context = {
            'assunto_adm': cls.assunto_adm.pk,
            'destino_adm': cls.processo.destino_adm,
            'oficiante': cls.processo.oficiante,
            'outro': cls.processo.outro,
            'email': cls.processo.email,
            'fone': cls.processo.fone,
            'observacao': cls.processo.observacao,
        }

        cls.response_unlogged = 'componentes/singles/core/Home.html', 200
        cls.response_without_perm_GET = '403.html', 403
        cls.response_without_perm_POST = '403.html', 403
        cls.response_policial_GET = 'componentes/shares/FormsCriarProcedimento.html', 200
        cls.response_policial_POST = '', 302
        cls.response_superior_GET = 'componentes/shares/FormsCriarProcedimento.html', 200
        cls.response_superior_POST = 'componentes/singles/processos/adm/detalhes/_DetalheGeral.html', 200

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user)

        assign_perm('adm.add_administrativo', cls.group_superior)
        assign_perm('adm.add_administrativo', cls.normal_user)

    def test_unlogged_GET(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_unlogged_POST(self):
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_logged_without_permission_GET(self):
        self.client.login(username=self.usuario.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_without_perm_GET[1])
        self.assertTemplateUsed(response, self.response_without_perm_GET[0])

    def test_logged_without_permission_POST(self):
        self.client.login(username=self.usuario.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_without_perm_POST[1])
        self.assertTemplateUsed(response, self.response_without_perm_POST[0])

    def test_logged_with_policial_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_policial_GET[1])
        self.assertTemplateUsed(response, self.response_policial_GET[0])

    def test_logged_with_policial_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context)
        self.assertEqual(response.status_code, self.response_policial_POST[1])

    def test_logged_with_superior_permission_GET(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_superior_GET[1])
        self.assertTemplateUsed(response, self.response_superior_GET[0])

    def test_logged_with_superior_permission_POST(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_superior_POST[1])
        self.assertTemplateUsed(response, self.response_superior_POST[0])


class AdministrativoListViewTestCase(SetUpTestViewsData, TestCase):

    def setUp(cls):
        cls.processo = AdministrativoFactory.create_batch(10, orgao_processo=cls.orgao, autor=cls.superior)
        cls.url = reverse('adm:listar_adm')

        cls.response_unlogged = 'componentes/singles/core/Home.html', 200
        cls.response_without_perm_GET = 'componentes/shares/ProcessosList.html', 200
        cls.response_without_perm_POST = ''
        cls.response_normal_user_GET = 'componentes/shares/ProcessosList.html', 200
        cls.response_normal_user_POST = ''
        cls.response_superior_GET = 'componentes/shares/ProcessosList.html', 200
        cls.response_superior_POST = ''

        cls.context = {}

    def test_unlogged_GET(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_unlogged_POST(self):
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_logged_without_permission_GET(self):
        self.client.login(username=self.usuario.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_without_perm_GET[1])
        self.assertTemplateUsed(response, self.response_without_perm_GET[0])

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_user_GET[1])
        self.assertTemplateUsed(response, self.response_normal_user_GET[0])

    def test_logged_with_superior_permission_GET(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_superior_GET[1])
        self.assertTemplateUsed(response, self.response_superior_GET[0])


class AdministrativoAjaxDatatableViewTestCase(SetUpTestViewsData, TestCase):

    def setUp(cls):
        cls.header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        cls.content_type = 'application/x-www-form-urlencoded'
        cls.data_initialize = {'action': 'initialize'}
        cls.data = ('draw=1&columns%5B0%5D%5Bdata%5D=&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D' +
                    '=false&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%' +
                    '5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=pk&columns%5B1%5D%5Bname%5D=p' +
                    'k&columns%5B1%5D%5Bsearchable%5D=false&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%' +
                    '5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%' +
                    '5D=observacao&columns%5B2%5D%5Bname%5D=observacao&columns%5B2%5D%5Bsearchable%5D=true&colu' +
                    'mns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bse' +
                    'arch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=criacao&columns%5B3%5D%5Bname%5D=criacao' +
                    '&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bs' +
                    'earch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=' +
                    'numero_processo&columns%5B4%5D%5Bname%5D=numero_processo&columns%5B4%5D%5Bsearchable%5D=tr' +
                    'ue&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5' +
                    'D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=oficiante&columns%5B5%5D%5Bname%5D' +
                    '=oficiante&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%' +
                    '5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%' +
                    '5Bdata%5D=destino_adm&columns%5B6%5D%5Bname%5D=destino_adm&columns%5B6%5D%5Bsearchable%5D=' +
                    'true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6' +
                    '%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=assunto_adm&columns%5B7%5D%' +
                    '5Bname%5D=assunto_adm&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%' +
                    '5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false' +
                    '&columns%5B8%5D%5Bdata%5D=outro&columns%5B8%5D%5Bname%5D=outro&columns%5B8%5D%5Bsearchable' +
                    '%5D=true&columns%5B8%5D%5Borderable%5D=false&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&column' +
                    's%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=acessar&columns%5B9%5D%5Bna' +
                    'me%5D=acessar&columns%5B9%5D%5Bsearchable%5D=false&columns%5B9%5D%5Borderable%5D=false&col' +
                    'umns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%' +
                    '5D%5Bcolumn%5D=3&order%5B0%5D%5Bdir%5D=desc&start=0&length=50&search%5Bvalue%5D=&search%5B' +
                    'regex%5D=false')

        cls.client = Client()
        AdministrativoFactory.create_batch(7)
        cls.processos = AdministrativoFactory.create_batch(10, orgao_processo=cls.orgao, autor=cls.superior)
        cls.url = reverse('adm:processos_adm_ajax')

        cls.response_unlogged = '403.html', 403

    def test_unlogged_GET(self):
        response = self.client.get(self.url, self.data_initialize, content_type=self.content_type, **self.header)
        self.assertEqual(response.status_code, 200)

    def test_unlogged_POST(self):
        response = self.client.post(self.url, self.data, content_type=self.content_type, **self.header)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_request_logged(self):
        self.client.login(username=self.superior.username, password=self.password)
        response_initialize = self.client.post(self.url, self.data_initialize, **self.header)
        response = self.client.post(self.url, self.data, content_type=self.content_type, **self.header)
        self.assertEqual(response_initialize.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['data']), 10)


class AdministrativoDetailViewTestCase(SetUpTestViewsData, TestCase):

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.superior)
        cls.url = reverse('adm:detalhe_processo_adm', kwargs={'pk': cls.processo.pk})

        cls.context = {}

        cls.response_unlogged = '403.html', 403
        cls.response_without_perm_GET = '403.html', 403
        cls.response_without_perm_POST = '403.html', 403
        cls.response_policial_GET = 'componentes/singles/processos/adm/detalhes/_DetalheGeral.html', 200
        cls.response_policial_POST = '', None
        cls.response_superior_GET = 'componentes/singles/processos/adm/detalhes/_DetalheGeral.html', 200
        cls.response_superior_POST = '', None

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

    def test_unlogged_GET(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_unlogged_POST(self):
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_logged_without_permission_GET(self):
        self.client.login(username=self.usuario.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_without_perm_GET[1])
        self.assertTemplateUsed(response, self.response_without_perm_GET[0])

    def test_logged_with_policial_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_policial_GET[1])
        self.assertTemplateUsed(response, self.response_policial_GET[0])

    def test_logged_with_superior_permission_GET(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_superior_GET[1])
        self.assertTemplateUsed(response, self.response_superior_GET[0])

    def test_logged_with_superior_permission_GET_invalid(self):
        self.client.login(username=self.superior.username, password=self.password)
        processo = AdministrativoFactory()
        url = reverse('adm:detalhe_processo_adm', kwargs={'pk': processo.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.response_without_perm_GET[1])
        self.assertTemplateUsed(response, self.response_without_perm_GET[0])

    def logged_with_superior_permission_GET_external_user(self):
        self.client.login(username=self.superior.username, password=self.password)
        processo = AdministrativoFactory()
        assign_perm("adm.view_adm", self.superior, processo)
        url = reverse('adm:detalhe_processo_adm', kwargs={'pk': processo.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, self.response_superior_GET[1])
        self.assertTemplateUsed(response, self.response_superior_GET[0])


class AdministrativoUpdateViewTestCase(SetUpTestViewsData, TestCase):

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.superior)
        cls.assunto_adm = AssuntoAdministrativoFactory()
        cls.url = reverse('adm:editar_processo_adm', kwargs={'pk': cls.processo.pk})

        cls.context = {
            'assunto_adm': cls.assunto_adm.pk,
            'destino_adm': cls.processo.destino_adm,
            'oficiante': cls.processo.oficiante,
            'outro': cls.processo.outro,
            'email': cls.processo.email,
            'fone': cls.processo.fone,
            'observacao': cls.processo.observacao,
            'arquivar': True,
        }

        cls.response_unlogged = 'componentes/singles/core/Home.html', 200
        cls.response_without_perm_GET = '403.html', 403
        cls.response_without_perm_POST = '403.html', 403
        cls.response_policial_GET = 'componentes/shares/FormsCriarProcedimento.html', 200
        cls.response_policial_POST = 'componentes/singles/processos/adm/detalhes/_DetalheGeral.html', 200
        cls.response_superior_GET = 'componentes/shares/FormsCriarProcedimento.html', 200
        cls.response_superior_POST = 'componentes/singles/processos/adm/detalhes/_DetalheGeral.html', 200

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm('adm.add_administrativo', cls.group_superior)
        assign_perm('adm.add_administrativo', cls.normal_user, cls.processo)

        assign_perm('adm.change_administrativo', cls.group_superior)
        assign_perm('adm.change_administrativo', cls.normal_user, cls.processo)

    def test_unlogged_GET(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_unlogged_POST(self):
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_logged_without_permission_GET(self):
        self.client.login(username=self.usuario.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_without_perm_GET[1])
        self.assertTemplateUsed(response, self.response_without_perm_GET[0])

    def test_logged_without_permission_POST(self):
        self.client.login(username=self.usuario.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_without_perm_POST[1])
        self.assertTemplateUsed(response, self.response_without_perm_POST[0])

    def test_logged_with_policial_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_policial_GET[1])
        self.assertTemplateUsed(response, self.response_policial_GET[0])

    def test_logged_with_policial_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_policial_POST[1])
        self.assertTemplateUsed(response, self.response_policial_POST[0])

    def test_logged_with_superior_permission_GET(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_superior_GET[1])
        self.assertTemplateUsed(response, self.response_superior_GET[0])

    def test_logged_with_superior_permission_POST(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_superior_POST[1])
        self.assertTemplateUsed(response, self.response_superior_POST[0])


class AdmExtratoPdfViewTestCase(SetUpTestViewsData, TestCase):

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.superior)
        cls.url = reverse('adm:extrato_pdf_adm', kwargs={'pk': cls.processo.pk})

        cls.response_unlogged = 'componentes/singles/core/Home.html', 200
        cls.response_without_perm_GET = 'componentes/singles/processos/adm/ExtratoPdf.html', 200
        cls.response_without_perm_POST = ''
        cls.response_policial_GET = 'componentes/singles/processos/adm/ExtratoPdf.html', 200
        cls.response_policial_POST = ''
        cls.response_superior_GET = 'componentes/singles/processos/adm/ExtratoPdf.html', 200
        cls.response_superior_POST = ''

        cls.context = {}

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm('adm.add_administrativo', cls.group_superior)
        assign_perm('adm.add_administrativo', cls.normal_user, cls.processo)

    def test_unlogged_GET(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_unlogged_POST(self):
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_logged_without_permission_GET(self):
        self.client.login(username=self.usuario.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_without_perm_GET[1])
        self.assertTemplateUsed(response, self.response_without_perm_GET[0])

    def test_logged_with_policial_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_policial_GET[1])
        self.assertTemplateUsed(response, self.response_policial_GET[0])

    def test_logged_with_superior_permission_GET(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_superior_GET[1])
        self.assertTemplateUsed(response, self.response_superior_GET[0])
