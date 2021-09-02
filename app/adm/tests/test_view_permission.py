
from account.tests.factories import ProfileFactory
from adm.tests.factories import AdministrativoFactory
from adm.tests.utils import SetUpTestViewAtoData
from core.permissions import GRUPO_ADMINISTRATIVO
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from guardian.shortcuts import assign_perm


class SelectUserPermissionAdmViewTestCase(SetUpTestViewAtoData, TestCase):

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.url = reverse('adm:select_user_adm', kwargs={'pk': cls.processo.pk})

        cls.batch = ProfileFactory.create_batch(10, orgao_link=cls.orgao)

        cls.context = {
            'usuarios': [f'{profile.user.pk}' for profile in cls.batch]
        }

        cls.response_unlogged = 'componentes/singles/core/Home.html', 200
        cls.response_without_perm_GET = '403.html', 403
        cls.response_without_perm_POST = '403.html', 403
        cls.response_policial_GET = '403.html', 403
        cls.response_policial_POST = '403.html', 403
        cls.response_superior_GET = 'componentes/shares/SelectUserPerm.html', 200
        cls.response_superior_POST = 'componentes/shares/PermForUser.html', 200

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user)

        assign_perm('adm.add_administrativo', cls.group_superior)
        assign_perm('adm.add_administrativo', cls.normal_user, cls.processo)

        cls.group = Group(name=GRUPO_ADMINISTRATIVO)
        cls.group.save()

        for profile in cls.batch:
            profile.user.groups.add(cls.group)

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


class SelectUserOrgaoExternoAdmViewTestCase(SetUpTestViewAtoData, TestCase):

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.url = reverse('adm:add_external_users_adm', kwargs={'pk': cls.processo.pk})

        cls.batch = ProfileFactory.create_batch(10)

        cls.context = {
            'usuarios': [f'{profile.user.pk}' for profile in cls.batch]
        }

        cls.response_unlogged = 'componentes/singles/core/Home.html', 200
        cls.response_without_perm_GET = '403.html', 403
        cls.response_without_perm_POST = '403.html', 403
        cls.response_policial_GET = '403.html', 403
        cls.response_policial_POST = '403.html', 403
        cls.response_superior_GET = 'componentes/shares/SelectUserPerm.html', 200
        cls.response_superior_POST = 'componentes/shares/PermForUser.html', 200

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user)

        assign_perm('adm.add_administrativo', cls.group_superior)
        assign_perm('adm.add_administrativo', cls.normal_user, cls.processo)

        cls.group = Group(name=GRUPO_ADMINISTRATIVO)
        cls.group.save()

        for profile in cls.batch:
            profile.user.groups.add(cls.group)

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


class PermissionAdmViewTestCase(SetUpTestViewAtoData, TestCase):

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.url = reverse('adm:select_perm_adm', kwargs={'pk': cls.processo.pk})

        cls.batch = ProfileFactory.create_batch(2, orgao_link=cls.orgao)

        cls.context = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-username': cls.batch[0].user.username,
            'form-1-username': cls.batch[1].user.username,
        }

        cls.response_unlogged = 'componentes/singles/core/Home.html', 200
        cls.response_without_perm_GET = '403.html', 403
        cls.response_without_perm_POST = '403.html', 403
        cls.response_policial_GET = '403.html', 403
        cls.response_policial_POST = '403.html', 403
        cls.response_superior_GET = 'componentes/shares/PermForUser.html', 200
        cls.response_superior_POST = 'componentes/singles/processos/adm/detalhes/_DetalheGeral.html', 200

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user)

        assign_perm('adm.add_administrativo', cls.group_superior)
        assign_perm('adm.add_administrativo', cls.normal_user, cls.processo)

        cls.group = Group(name=GRUPO_ADMINISTRATIVO)
        cls.group.save()

        for profile in cls.batch:
            profile.user.groups.add(cls.group)

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
