import json

from account.tests.factories import OrgaoFactory, ProfileFactory
from adm.tests.factories import AdministrativoFactory
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse
from inteligencia.tests.factories import InteligenciaFactory
from interceptacao.tests.factories import InterceptacaoFactory
from lab.tests.factories import LabFactory
from auditoria.models import BuscaAuditoria
from quebra.tests.factories import QuebraFactory


class BuscaMultiOrgaosApiViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.password = 'Django01'

        cls.orgao0 = OrgaoFactory()
        orgao0_perm = Permission.objects.get(codename='access_ADMINISTRATIVO')
        cls.orgao0.permissions.add(orgao0_perm)

        cls.orgao1 = OrgaoFactory()
        orgao1_perm = Permission.objects.get(codename='access_INTERCEPTACOES')
        cls.orgao1.permissions.add(orgao1_perm)

        cls.orgao2 = OrgaoFactory()
        orgao2_perms = Permission.objects.filter(
            codename__in=[
                'access_LAB_LD',
                'access_INTERCEPTACOES',
                'access_QUEBRAS',
                'access_INTELIGENCIA',
                'access_ADMINISTRATIVO'])
        cls.orgao2.permissions.add(*orgao2_perms)

        profile_orgao0 = ProfileFactory(orgao_link=cls.orgao0)
        cls.usuario_orgao0 = profile_orgao0.user
        cls.usuario_orgao0.set_password(cls.password)
        cls.usuario_orgao0.save()

        profile_orgao1 = ProfileFactory(orgao_link=cls.orgao1)
        cls.usuario_orgao1 = profile_orgao1.user
        cls.usuario_orgao1.set_password(cls.password)
        cls.usuario_orgao1.save()

        profile_orgao2 = ProfileFactory(orgao_link=cls.orgao2)
        cls.usuario_orgao2 = profile_orgao2.user
        cls.usuario_orgao2.set_password(cls.password)
        cls.usuario_orgao2.save()

    def setUp(cls):
        cls.processo_adm_orgao0 = AdministrativoFactory.create_batch(9, orgao_processo=cls.orgao0)[0]
        cls.processo_inter_orgao1 = InterceptacaoFactory.create_batch(8, orgao_processo=cls.orgao1)[0]

        cls.processo_adm_orgao2 = AdministrativoFactory.create_batch(7, orgao_processo=cls.orgao2)[0]
        cls.processo_inter_orgao2 = InterceptacaoFactory.create_batch(6, orgao_processo=cls.orgao2)[0]
        InteligenciaFactory.create_batch(5, orgao_processo=cls.orgao2)
        LabFactory.create_batch(4, orgao_processo=cls.orgao2)
        QuebraFactory.create_batch(3, orgao_processo=cls.orgao2)

        cls.url = reverse('busca_multi_orgaos_api')

        cls.response_unlogged = 'componentes/singles/core/Home.html', 200

    def test_unlogged_GET(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_unlogged_POST(self):
        response = self.client.post(self.url, {}, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_logged_with_access_administrativo_permission(self):
        self.client.login(username=self.usuario_orgao0.username, password=self.password)
        query = self.processo_adm_orgao0.numero_processo
        response = self.client.get(self.url, {'q': query}, follow=True)
        data = [self.adm_serializer(self.processo_adm_orgao0)]
        qs_buscas = BuscaAuditoria.objects.filter(query=query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['results'], data)
        self.assertEqual(qs_buscas.count(), 1)

    def test_logged_with_access_interceptacoes_permission(self):
        self.client.login(username=self.usuario_orgao1.username, password=self.password)
        query = self.processo_inter_orgao1.numero_processo
        response = self.client.get(self.url, {'q': query}, follow=True)
        data = [self.inter_serializer(self.processo_inter_orgao1)]
        qs_buscas = BuscaAuditoria.objects.filter(query=query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['results'], data)
        self.assertEqual(qs_buscas.count(), 1)

    def test_logged_with_access_all_permission(self):
        self.client.login(username=self.usuario_orgao2.username, password=self.password)
        query = self.processo_adm_orgao2.numero_processo
        response = self.client.get(self.url, {'q': query}, follow=True)
        data = [self.adm_serializer(self.processo_adm_orgao2)]
        qs_buscas = BuscaAuditoria.objects.filter(query=query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['results'], data)
        self.assertEqual(qs_buscas.count(), 1)

    def test_search_orgao1_process_with_orgao0_user(self):
        self.client.login(username=self.usuario_orgao0.username, password=self.password)
        query = self.processo_inter_orgao1.numero_processo
        response = self.client.get(self.url, {'q': query}, follow=True)
        qs_buscas = BuscaAuditoria.objects.filter(query=query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['results'], [])
        self.assertEqual(qs_buscas.count(), 1)

    def test_search_orgao0_process_with_orgao1_user(self):
        self.client.login(username=self.usuario_orgao1.username, password=self.password)
        query = self.processo_adm_orgao0.numero_processo
        response = self.client.get(self.url, {'q': query}, follow=True)
        qs_buscas = BuscaAuditoria.objects.filter(query=query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['results'], [])
        self.assertEqual(qs_buscas.count(), 1)

    def test_search_orgao1_process_with_orgao2_user(self):
        self.client.login(username=self.usuario_orgao2.username, password=self.password)
        query = self.processo_inter_orgao1.numero_processo
        response = self.client.get(self.url, {'q': query}, follow=True)
        qs_buscas = BuscaAuditoria.objects.filter(query=query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['results'], [])
        self.assertEqual(qs_buscas.count(), 1)

    def test_search_orgao0_process_with_orgao2_user(self):
        self.client.login(username=self.usuario_orgao2.username, password=self.password)
        query = self.processo_adm_orgao0.numero_processo
        response = self.client.get(self.url, {'q': query}, follow=True)
        qs_buscas = BuscaAuditoria.objects.filter(query=query)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['results'], [])
        self.assertEqual(qs_buscas.count(), 1)

    def adm_serializer(self, processo):
        return {
                'title': 'Administrativo - Processo nº {}'.format(processo.numero_processo),
                'description': '',
                'url': processo.get_absolute_url(),
                'meta': {
                    'get_destino': processo.get_destino(),
                    'get_origem': processo.get_origem(),
                    'get_tipo_procedimento': processo.get_tipo_procedimento()
                }
            }

    def inter_serializer(self, processo):
        return {
                'title': 'Operação {} - nº {}'.format(processo.nome_operacao.upper(), processo.numero_processo),
                'description': '',
                'url': processo.get_absolute_url(),
                'meta': {
                    'get_procedimento': processo.get_procedimento(),
                    'get_origem': processo.get_origem(),
                    'get_tipo_procedimento': processo.get_tipo_procedimento()
                }
            }


class BuscaMultiOrgaosViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.password = 'Django01'

        cls.orgao0 = OrgaoFactory()
        orgao0_perm = Permission.objects.get(codename='access_ADMINISTRATIVO')
        cls.orgao0.permissions.add(orgao0_perm)

        profile_orgao0 = ProfileFactory(orgao_link=cls.orgao0)
        cls.usuario_orgao0 = profile_orgao0.user
        cls.usuario_orgao0.set_password(cls.password)
        cls.usuario_orgao0.save()

    def setUp(cls):
        cls.processo_adm_orgao0 = AdministrativoFactory.create_batch(9, orgao_processo=cls.orgao0)[0]

        cls.url = reverse('busca_multi_orgaos')

        cls.response_unlogged = 'componentes/singles/core/Home.html', 200
        cls.response_logged = 'componentes/singles/buscas/_ResultadoBusca.html', 200

    def test_unlogged_GET(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_unlogged_POST(self):
        response = self.client.post(self.url, {}, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_logged_search(self):
        self.client.login(username=self.usuario_orgao0.username, password=self.password)
        query = self.processo_adm_orgao0.numero_processo
        response = self.client.get(self.url, {'q': query}, follow=True)
        qs_buscas = BuscaAuditoria.objects.filter(query=query)
        self.assertEqual(response.status_code, self.response_logged[1])
        self.assertTemplateUsed(response, self.response_logged[0])
        self.assertEqual(qs_buscas.count(), 1)
