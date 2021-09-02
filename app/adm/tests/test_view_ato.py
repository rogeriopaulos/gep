from adm.tests.factories import (
    AdministrativoFactory,
    DespachoAdmFactory,
    DocumentoAdmFactory,
    LocalizacaoStatusAdmFactory,
    MidiaAdmFactory,
    OficioExternoAdmFactory,
    OficioInternoAdmFactory,
    StatusAdmFactory
)
from adm.tests.utils import SetUpTestViewAtoData
from core.tests.factories import ConteudoOficioExternoFactory, ConteudoOficioInternoFactory, MotivoVinculoFactory
from django.test import TestCase
from django.urls import reverse
from guardian.shortcuts import assign_perm


class AtoAdmCreateViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:add_ofinterno_adm'
    model_factory = OficioInternoAdmFactory
    permission = 'adm.add_administrativo'

    response_arquivado_GET = 'componentes/singles/core/Arquivado.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.superior, arquivar=True)
        cls.ato = cls.model_factory.build(
            processo=cls.processo, autor=cls.superior, autoridade=cls.superior.get_full_name())
        cls.url = reverse(cls.view_name, kwargs={'pk': cls.processo.pk, 'tipo_ato': cls.ato.tipo_ato})

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm(cls.permission, cls.group_superior)

    def test_processo_arquivado_GET(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_arquivado_GET[1])
        self.assertTemplateUsed(response, self.response_arquivado_GET[0])


class AtoAdmUpdateViewTestCase(SetUpTestViewAtoData, TestCase):
    view_name = 'adm:editar_ofinterno_adm'
    model_factory = OficioInternoAdmFactory
    permission = 'adm.change_administrativo'

    response_arquivado_GET = 'componentes/singles/core/Arquivado.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.superior, arquivar=True)
        cls.ato = cls.model_factory(processo=cls.processo, autor=cls.superior, autoridade=cls.superior.get_full_name())
        cls.url = reverse(cls.view_name,
                          kwargs={'pk': cls.ato.pk})

        assign_perm(cls.permission, cls.group_superior, cls.processo)
        assign_perm(cls.permission, cls.group_superior, cls.processo)

    def test_processo_arquivado_GET(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_arquivado_GET[1])
        self.assertTemplateUsed(response, self.response_arquivado_GET[0])


class OfInternoCreateViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:add_ofinterno_adm'
    model_factory = OficioInternoAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '403.html', 403
    response_normal_GET = 'componentes/shares/FormGeral.html', 200
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = 'componentes/shares/FormGeral.html', 200
    response_superior_POST = 'componentes/shares/NotifyForm.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = cls.model_factory.build(processo=cls.processo)
        cls.conteudo = ConteudoOficioInternoFactory()
        cls.url = reverse(cls.view_name, kwargs={'pk': cls.processo.pk, 'tipo_ato': cls.ato.tipo_ato})

        cls.context = {
            'destino': cls.ato.destino,
            'autoridade': cls.superior.profile.pk,
            'conteudo': cls.conteudo.pk
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmCreateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmCreateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class OfInternoUpdateViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:editar_ofinterno_adm'
    model_factory = OficioInternoAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '403.html', 403
    response_normal_GET = 'componentes/shares/FormGeral.html', 200
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = 'componentes/shares/FormGeral.html', 200
    response_superior_POST = 'componentes/shares/NotifyForm.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = cls.model_factory(
            processo=cls.processo,
            autor=cls.normal_user,
            autoridade=cls.superior.get_full_name()
        )
        cls.url = reverse(cls.view_name, kwargs={'pk': cls.ato.pk})

        cls.context = {
            'destino': cls.ato.destino,
            'autoridade': cls.superior.profile.pk,
            'conteudo': cls.ato.conteudo.pk
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class OfInternoArquivoUpdateViewTestCase(SetUpTestViewAtoData, TestCase):
    view_name = 'adm:editar_ofinterno_arq_adm'
    model_factory = OficioInternoAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '403.html', 403
    response_normal_GET = 'componentes/shares/DadosPopup.html', 200
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = 'componentes/shares/DadosPopup.html', 200
    response_superior_POST = 'componentes/shares/NotifyForm.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = cls.model_factory(
            processo=cls.processo,
            autor=cls.normal_user,
            autoridade=cls.superior.get_full_name()
        )
        cls.url = reverse(cls.view_name, kwargs={'pk': cls.ato.pk})

        cls.context = {
            'arquivo': cls.ato.arquivo,
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class OfInternoAdmConfirmViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:editar_confirmacao_adm'
    model_factory = OficioInternoAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '403.html', 403
    response_normal_GET = 'componentes/shares/ConfirmacaoPopup.html', 200
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = 'componentes/shares/ConfirmacaoPopup.html', 200
    response_superior_POST = 'componentes/shares/NotifyForm.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = cls.model_factory(
            processo=cls.processo,
            autor=cls.normal_user,
            autoridade=cls.superior.get_full_name()
        )
        cls.url = reverse(cls.view_name, kwargs={'pk': cls.ato.pk})

        cls.context = {
            'destino': cls.ato.destino,
            'autoridade': cls.superior.profile.pk,
            'conteudo': cls.ato.conteudo.pk
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class OfInternoAdmDataEnvioViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:editar_dataenvio_adm'
    model_factory = OficioInternoAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '403.html', 403
    response_normal_GET = 'componentes/shares/DataEnvioPopup.html', 200
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = 'componentes/shares/DataEnvioPopup.html', 200
    response_superior_POST = 'componentes/shares/NotifyForm.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = cls.model_factory(
            processo=cls.processo,
            autor=cls.normal_user,
            autoridade=cls.superior.get_full_name()
        )
        cls.url = reverse(cls.view_name, kwargs={'pk': cls.ato.pk})

        cls.context = {
            'destino': cls.ato.destino,
            'autoridade': cls.superior.profile.pk,
            'conteudo': cls.ato.conteudo.pk
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class OfExternoAdmCreateViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:add_ofexterno_adm'
    model_factory = OficioExternoAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '403.html', 403
    response_normal_GET = 'componentes/shares/FormGeral.html', 200
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = 'componentes/shares/FormGeral.html', 200
    response_superior_POST = 'componentes/shares/NotifyForm.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = cls.model_factory(processo=cls.processo)
        cls.url = reverse(cls.view_name, kwargs={'pk': cls.processo.pk, 'tipo_ato': cls.ato.tipo_ato})

        cls.context = {
            'origem': cls.ato.origem,
            'arquivo': cls.ato.arquivo,
            'num_oficio': cls.ato.num_oficio,
            'conteudo': cls.ato.conteudo.pk,
            'data_recebimento': cls.ato.data_recebimento,
            'nome_recebimento': cls.ato.nome_recebimento
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmCreateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmCreateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class OfExternoAdmUpdateViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:editar_ofexterno_adm'
    model_factory = OficioExternoAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '403.html', 403
    response_normal_GET = 'componentes/shares/FormGeral.html', 200
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = 'componentes/shares/FormGeral.html', 200
    response_superior_POST = 'componentes/shares/NotifyForm.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = cls.model_factory(processo=cls.processo)
        cls.url = reverse(cls.view_name,
                          kwargs={'pk': cls.ato.pk})
        conteudo_externo = ConteudoOficioExternoFactory()

        cls.context = {
            'num_oficio': cls.ato.num_oficio,
            'origem': cls.ato.origem,
            'conteudo': conteudo_externo.pk,
            'outros': cls.ato.outros,
            'data_recebimento': cls.ato.data_recebimento,
            'nome_recebimento': cls.ato.nome_recebimento,
            'arquivo': cls.ato.arquivo,
            'descricao': cls.ato.descricao,
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class DespachoAdmCreateViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:add_despacho_adm'
    model_factory = DespachoAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '403.html', 403
    response_normal_GET = '403.html', 403
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = 'componentes/shares/CKEditorConteudo.html', 200
    response_superior_POST = 'componentes/shares/NotifyForm.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = cls.model_factory.build(processo=cls.processo)
        cls.url = reverse(cls.view_name,
                          kwargs={'pk': cls.processo.pk, 'tipo_ato': cls.ato.tipo_ato})

        cls.context = {
            'conteudo': cls.ato.conteudo,
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmCreateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmCreateViewTestCase.permission, cls.normal_user)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class DespachoAdmUpdateViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:editar_despacho_adm'
    model_factory = DespachoAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '404.html', 404
    response_normal_GET = 'componentes/shares/CKEditorConteudo.html', 200
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = '404.html', 404
    response_superior_POST = '404.html', 404

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = cls.model_factory(processo=cls.processo, autor=cls.normal_user)
        cls.url = reverse(cls.view_name,
                          kwargs={'pk': cls.ato.pk})

        cls.context = {
            'conteudo': cls.ato.conteudo,
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class StatusAdmCreateViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:add_status_adm'
    model_factory = StatusAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '403.html', 403
    response_normal_GET = 'componentes/shares/FormGeral.html', 200
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = 'componentes/shares/FormGeral.html', 200
    response_superior_POST = 'componentes/shares/NotifyForm.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = cls.model_factory.build(processo=cls.processo, autor=cls.normal_user)
        cls.url = reverse(cls.view_name,
                          kwargs={'pk': cls.processo.pk, 'tipo_ato': cls.ato.tipo_ato})
        localizacao_adm = LocalizacaoStatusAdmFactory()

        cls.context = {
            'localizacao': localizacao_adm.pk,
            'situacao': cls.ato.situacao,
            'outros': cls.ato.outros,
            'descricao': cls.ato.descricao,
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmCreateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmCreateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class StatusAdmUpdateViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:editar_status_adm'
    model_factory = StatusAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '403.html', 403
    response_normal_GET = 'componentes/shares/FormGeral.html', 200
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = 'componentes/shares/FormGeral.html', 200
    response_superior_POST = 'componentes/shares/NotifyForm.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = cls.model_factory(processo=cls.processo, autor=cls.normal_user)
        cls.url = reverse(cls.view_name,
                          kwargs={'pk': cls.ato.pk})
        localizacao_adm = LocalizacaoStatusAdmFactory()

        cls.context = {
            'localizacao': localizacao_adm.pk,
            'situacao': cls.ato.situacao,
            'outros': cls.ato.outros,
            'descricao': cls.ato.descricao,
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class GravacaoAdmCreateViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:add_gravacao_adm'
    model_factory = MidiaAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '403.html', 403
    response_normal_GET = 'componentes/shares/FormGeral.html', 200
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = 'componentes/shares/FormGeral.html', 200
    response_superior_POST = 'componentes/shares/NotifyForm.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = MidiaAdmFactory.build(processo=cls.processo)
        cls.tipo_gravacao_link = MidiaAdmFactory(processo=cls.processo).tipo_gravacao_link
        cls.url = reverse(cls.view_name,
                          kwargs={'pk': cls.processo.pk, 'tipo_ato': cls.ato.tipo_ato})

        cls.context = {
            'destino': cls.ato.destino,
            'solicitante': cls.ato.solicitante,
            'tipo_gravacao_link': cls.tipo_gravacao_link.pk,
            'autor': cls.normal_user.pk
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmCreateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmCreateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class DocumentoCreateViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:add_documento_adm'
    model_factory = DocumentoAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '403.html', 403
    response_normal_GET = 'componentes/shares/FormGeral.html', 200
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = 'componentes/shares/FormGeral.html', 200
    response_superior_POST = 'componentes/shares/NotifyForm.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = cls.model_factory.build(processo=cls.processo, autor=cls.normal_user)
        cls.url = reverse(cls.view_name,
                          kwargs={'pk': cls.processo.pk, 'tipo_ato': cls.ato.tipo_ato})

        cls.context = {
            'nome_doc': cls.ato.nome_doc,
            'motivo_anulacao': cls.ato.motivo_anulacao,
            'documento': cls.ato.documento,
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmCreateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmCreateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class DocumentoUpdateViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:editar_documento_adm'
    model_factory = DocumentoAdmFactory

    response_unlogged = 'componentes/singles/core/Home.html', 200
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '404.html', 404
    response_normal_GET = 'componentes/shares/FormGeral.html', 200
    response_normal_POST = 'componentes/shares/NotifyForm.html', 200
    response_superior_GET = '404.html', 404
    response_superior_POST = '404.html', 404

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.normal_user, arquivar=False)
        cls.ato = cls.model_factory(processo=cls.processo, autor=cls.normal_user)
        cls.url = reverse(cls.view_name,
                          kwargs={'pk': cls.ato.pk})

        cls.context = {
            'nome_doc': cls.ato.nome_doc,
            'motivo_anulacao': cls.ato.motivo_anulacao,
            'documento': cls.ato.documento,
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_normal_user_permission_GET(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_normal_GET[1])
        self.assertTemplateUsed(response, self.response_normal_GET[0])

    def test_logged_with_normal_user_permission_POST(self):
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_normal_POST[1])
        self.assertTemplateUsed(response, self.response_normal_POST[0])

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


class AnularAtoViewTestCase(SetUpTestViewAtoData, TestCase):

    view_name = 'adm:anular_ato'
    model_factory = MidiaAdmFactory

    response_unlogged = '403.html', 403
    response_without_perm_GET = '403.html', 403
    response_without_perm_POST = '403.html', 403
    response_normal_GET = '', 000
    response_normal_POST = '', 000
    response_superior_GET = 'componentes/shares/ModalAnulacao.html', 200
    response_superior_POST = 'componentes/singles/processos/adm/detalhes/_DetalheGeral.html', 200

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.superior, arquivar=False)
        cls.ato = cls.model_factory(autor=cls.superior, processo=cls.processo, anulado=False)
        cls.url = reverse(cls.view_name, kwargs={'pk': cls.ato.pk})

        cls.context = {
            'motivo_anulacao': cls.ato.motivo_anulacao,
            'tipo_ato': cls.ato.tipo_ato
        }

        assign_perm('adm.view_administrativo', cls.group_superior)
        assign_perm('adm.view_administrativo', cls.normal_user, cls.processo)

        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.group_superior)
        assign_perm(AtoAdmUpdateViewTestCase.permission, cls.normal_user, cls.processo)

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

    def test_logged_with_superior_permission_POST(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_superior_POST[1])
        self.assertTemplateUsed(response, self.response_superior_POST[0])

    def test_logged_with_superior_permission_GET(self):
        self.client.login(username=self.superior.username, password=self.password)
        url = reverse('adm:detalhe_processo_adm', kwargs={'pk': self.processo.pk})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, self.response_superior_GET[1])
        self.assertTemplateUsed(response, self.response_superior_GET[0])


class VincularProcessosCreateViewTestCase(SetUpTestViewAtoData, TestCase):

    def setUp(cls):
        cls.processo = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.superior, arquivar=False)
        cls.processo_b = AdministrativoFactory(orgao_processo=cls.orgao, autor=cls.superior, arquivar=False)
        cls.url = reverse('adm:vincular_processos', kwargs={'pk': cls.processo_b.pk})
        cls.motivo = MotivoVinculoFactory(motivo='Um motivo qualquer.')

        cls.context = {
            "processo_b": cls.processo_b.pk,
            "motivo_vinculo": cls.motivo.pk
        }

        cls.response_unlogged = '403.html', 403
        cls.response_without_perm_GET = '403.html', 403
        cls.response_without_perm_POST = '403.html', 403
        cls.response_normal_GET = '', 000
        cls.response_normal_POST = '', 000
        cls.response_superior_GET = 'componentes/shares/VincularProcessos.html', 200
        cls.response_superior_POST = 'componentes/singles/processos/adm/detalhes/_DetalheGeral.html', 200

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

    def test_logged_without_permission_POST(self):
        self.client.login(username=self.usuario.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_without_perm_POST[1])
        self.assertTemplateUsed(response, self.response_without_perm_POST[0])

    def test_logged_with_superior_permission_POST(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_superior_POST[1])
        self.assertTemplateUsed(response, self.response_superior_POST[0])

    def test_logged_with_superior_permission_GET(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_superior_GET[1])
        self.assertTemplateUsed(response, self.response_superior_GET[0])

    def test_logged_with_superior_permission_POST_invalid(self):
        self.client.login(username=self.superior.username, password=self.password)
        processo_b = AdministrativoFactory(arquivar=False)
        response = self.client.post(self.url, {"processo_b": processo_b.pk, "motivo_vinculo": self.motivo.pk})
        self.assertEqual(
            response.context['form'].errors,
            {'processo_b': ['Faça uma escolha válida. Sua escolha não é uma das disponíveis.']}
        )
        self.assertEqual(response.status_code, self.response_superior_GET[1])
        self.assertTemplateUsed(response, self.response_superior_GET[0])
