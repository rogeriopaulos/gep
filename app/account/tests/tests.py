
from account.tests.factories import OrgaoFactory, ProfileFactory
from adm.tests.factories import AdministrativoFactory
from django.contrib.auth.models import Group, Permission
from django.test import Client, TestCase
from django.urls import reverse
from guardian.shortcuts import assign_perm



class ChangeProfileTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.password = 'Django01'

        PERMISSOES_ORGAO = ['access_ADMINISTRATIVO']
        permissions_orgao = Permission.objects.filter(
            content_type__app_label='account',
            content_type__model='orgao',
            codename__in=PERMISSOES_ORGAO
        )
        cls.orgao0 = OrgaoFactory()
        cls.orgao0.permissions.add(*permissions_orgao)
        cls.orgao1 = OrgaoFactory()
        cls.orgao1.permissions.add(*permissions_orgao)

        cls.profile0 = ProfileFactory(orgao_link=cls.orgao0)
        cls.user0 = cls.profile0.user
        cls.user0.set_password(cls.password)
        cls.user0.save()

        perms = [
            'add_administrativo',
            'view_administrativo',
            'change_administrativo'
        ]

        perm_qs = Permission.objects.filter(content_type__app_label='adm', codename__in=perms)

        GRUPO_ADM = 'ADMINISTRATIVO'
        cls.group = Group(name=GRUPO_ADM)
        cls.group.save()
        cls.group.permissions.add(*perm_qs)

        cls.user0.groups.add(cls.group)

    def setUp(cls):
        processos = AdministrativoFactory.create_batch(10, orgao_processo=cls.orgao0)
        cls.processo = processos[-1]
        cls.processo_url = reverse("adm:detalhe_processo_adm", kwargs={"pk": cls.processo.pk})

        assign_perm('adm.view_administrativo', cls.user0, cls.processo)

        cls.response_without_perm_GET = '403.html', 403
        cls.response_with_perm_GET = 'componentes/singles/processos/adm/detalhes/_DetalheGeral.html', 200

    def test_access_with_user_orgao_not_changed(self):
        self.client.login(username=self.user0.username, password=self.password)
        response = self.client.get(self.processo_url)
        self.assertEqual(response.status_code, self.response_with_perm_GET[1])
        self.assertTemplateUsed(response, self.response_with_perm_GET[0])

    def test_access_with_user_orgao_changed(self):
        self.profile0.orgao_link = self.orgao1
        self.profile0.save()
        self.client.login(username=self.user0.username, password=self.password)
        response = self.client.get(self.processo_url)
        self.assertEqual(response.status_code, self.response_without_perm_GET[1])
        self.assertTemplateUsed(response, self.response_without_perm_GET[0])
