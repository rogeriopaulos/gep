
from account.tests.factories import ProfileFactory
from adm.tests.factories import OficioInternoAdmFactory
from core import permissions
from django.test import TestCase
from django.urls import reverse
from guardian.shortcuts import assign_perm
from inteligencia.tests.factories import OficioInternoIntelFactory
from interceptacao.tests.factories import ControlEmpresasInterFactory, OfEmpresasInterFactory
from lab.tests.factories import SoliciacaoLabFactory
from quebra.tests.factories import ControlEmpresasQuebraFactory, OfEmpresasQuebraFactory

from ..models import TelegramUser
from .factories import TelegramUserFactory
from .utils import SetUpTestData


class NotifyTestCaseBase:

    def setUp(cls):

        profiles_batch = ProfileFactory.create_batch(3, orgao_link=cls.orgao)
        users_batch = [profile.user for profile in profiles_batch]
        assign_perm(cls.view_permission, users_batch, cls.processo)
        cls.context = {"usuarios": [user.id for user in users_batch]}
        assign_perm(cls.view_permission, cls.group_superior)
        assign_perm(cls.add_permission, cls.group_superior)

        template_processo = f'componentes/singles/processos/{cls.app_template_folder}/detalhes/_DetalheGeral.html'

        cls.response_unlogged = 'componentes/singles/core/Home.html', 200
        cls.response_without_perm_GET = '403.html', 403
        cls.response_without_perm_POST = '403.html', 403

        cls.response_policial_GET = 'componentes/shares/NotifyForm.html', 200
        cls.response_policial_invalid_GET = '403.html', 403
        cls.response_policial_POST = template_processo, 200

        cls.response_superior_GET = 'componentes/shares/NotifyForm.html', 200
        cls.response_superior_invalid_GET = '403.html', 403
        cls.response_superior_POST = template_processo, 200
        cls.response_invalid_POST = 'componentes/shares/NotifyForm.html', 200

    def test_unlogged_GET(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_unlogged[1])
        self.assertTemplateUsed(response, self.response_unlogged[0])

    def test_unlogged_POST(self):
        response = self.client.post(self.url, {}, follow=True)
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
        assign_perm(self.view_permission, self.normal_user, self.processo)
        assign_perm(self.add_permission, self.normal_user, self.processo)
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_policial_GET[1])
        self.assertTemplateUsed(response, self.response_policial_GET[0])

    def test_logged_with_policial_externo_permission_valid_GET(self):
        self.normal_user.profile.orgao_link = self.orgao2
        self.normal_user.save()
        assign_perm(self.view_permission, self.normal_user, self.processo)
        assign_perm(self.add_permission, self.normal_user, self.processo)
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_policial_GET[1])
        self.assertTemplateUsed(response, self.response_policial_GET[0])

    def test_logged_with_policial_externo_permission_invalid_GET(self):
        self.normal_user.profile.orgao_link = self.orgao2
        self.normal_user.save()
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_policial_invalid_GET[1])
        self.assertTemplateUsed(response, self.response_policial_invalid_GET[0])

    def test_logged_with_policial_permission_POST(self):
        assign_perm(self.view_permission, self.normal_user, self.processo)
        assign_perm(self.add_permission, self.normal_user, self.processo)
        self.client.login(username=self.normal_user.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_policial_POST[1])
        self.assertTemplateUsed(response, self.response_policial_POST[0])

    def test_logged_with_superior_permission_GET(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_superior_GET[1])
        self.assertTemplateUsed(response, self.response_superior_GET[0])

    def test_logged_with_superior_externo_permission_valid_GET(self):
        self.superior.profile.orgao_link = self.orgao2
        self.superior.save()
        assign_perm(self.view_permission, self.superior, self.processo)
        assign_perm(self.add_permission, self.superior, self.processo)
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_superior_GET[1])
        self.assertTemplateUsed(response, self.response_superior_GET[0])

    def test_logged_with_superior_externo_permission_invalid_GET(self):
        self.superior.profile.orgao_link = self.orgao2
        self.superior.save()
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, self.response_superior_invalid_GET[1])
        self.assertTemplateUsed(response, self.response_superior_invalid_GET[0])

    def test_logged_with_superior_permission_POST(self):
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_superior_POST[1])
        self.assertTemplateUsed(response, self.response_superior_POST[0])

    def test_logged_with_superior_permission_invalid_POST(self):
        self.context['usuarios'].append(ProfileFactory().user.id)
        self.client.login(username=self.superior.username, password=self.password)
        response = self.client.post(self.url, self.context, follow=True)
        self.assertEqual(response.status_code, self.response_invalid_POST[1])
        self.assertTemplateUsed(response, self.response_invalid_POST[0])


class NotifyAtoFromLabTestCase(NotifyTestCaseBase, SetUpTestData, TestCase):

    nome_grupo_superior = 'COORDENADOR DO LAB'
    orgao_permission_required = 'access_LAB_LD'
    view_permission = 'lab.view_lab'
    add_permission = 'lab.add_lab'
    app_template_folder = 'lab'

    def setUp(cls):
        ato = SoliciacaoLabFactory(
            processo__orgao_processo=cls.orgao, autor=cls.superior, processo__arquivar=False, tipo_ato=1)
        cls.url = reverse("notifier:ato_lab", kwargs={"model_pk": ato.pk})
        cls.processo = ato.processo

        super().setUp()


class NotifyAtoFromAdmTestCase(NotifyTestCaseBase, SetUpTestData, TestCase):

    nome_grupo_superior = 'COORDENADOR ADMINISTRATIVO'
    orgao_permission_required = 'access_ADMINISTRATIVO'
    view_permission = 'adm.view_administrativo'
    add_permission = 'adm.add_administrativo'
    app_template_folder = 'adm'

    def setUp(cls):
        ato = OficioInternoAdmFactory(
            processo__orgao_processo=cls.orgao, processo__arquivar=False, autoridade=cls.superior, autor=cls.superior)
        cls.url = reverse("notifier:ato_adm", kwargs={"model_pk": ato.pk})
        cls.processo = ato.processo

        super().setUp()


class NotifyAtoFromQuebraTestCase(NotifyTestCaseBase, SetUpTestData, TestCase):

    nome_grupo_superior = 'COORDENADOR DE INTERCEPTAÇÃO/QUEBRA'
    orgao_permission_required = 'access_QUEBRAS'
    view_permission = 'quebra.view_quebra'
    add_permission = 'quebra.add_quebra'
    app_template_folder = 'quebra'

    def setUp(cls):
        ato = ControlEmpresasQuebraFactory(
            processo__orgao_processo=cls.orgao, autor=cls.superior, processo__arquivar=False, tipo_ato=1)
        cls.url = reverse("notifier:ato_quebra", kwargs={"model_pk": ato.pk})
        cls.processo = ato.processo

        super().setUp()


class NotifyAtoFromInteligenciaTestCase(NotifyTestCaseBase, SetUpTestData, TestCase):

    nome_grupo_superior = 'COORDENADOR DE INTELIGÊNCIA'
    orgao_permission_required = 'access_INTELIGENCIA'
    view_permission = 'inteligencia.view_inteligencia'
    add_permission = 'inteligencia.add_inteligencia'
    app_template_folder = 'intel'

    def setUp(cls):
        ato = OficioInternoIntelFactory(
            processo__orgao_processo=cls.orgao, autor=cls.superior, processo__arquivar=False, tipo_ato=1)
        cls.url = reverse("notifier:ato_intel", kwargs={"model_pk": ato.pk})
        cls.processo = ato.processo

        super().setUp()


class NotifyAtoFromInterceptacaoTestCase(NotifyTestCaseBase, SetUpTestData, TestCase):

    nome_grupo_superior = permissions.GRUPO_SUPERIOR_INTERCEPTACAO_QUEBRA
    orgao_permission_required = 'access_INTERCEPTACOES'
    view_permission = 'interceptacao.view_interceptacao'
    add_permission = 'interceptacao.add_interceptacao'
    app_template_folder = 'inter'

    def setUp(cls):
        ato = ControlEmpresasInterFactory(
            processo__orgao_processo=cls.orgao, autor=cls.superior, processo__arquivar=False, tipo_ato=1)
        cls.url = reverse("notifier:ato_inter", kwargs={"model_pk": ato.pk})
        cls.processo = ato.processo

        super().setUp()


class NotifyOficioFromQuebraTestCase(NotifyTestCaseBase, SetUpTestData, TestCase):

    nome_grupo_superior = 'COORDENADOR DE INTERCEPTAÇÃO/QUEBRA'
    orgao_permission_required = 'access_QUEBRAS'
    view_permission = 'quebra.view_quebra'
    add_permission = 'quebra.add_quebra'
    app_template_folder = 'quebra'

    def setUp(cls):
        oficio = OfEmpresasQuebraFactory(
            controlempresasquebra__processo__orgao_processo=cls.orgao,
            modificador=None,
            controlempresasquebra__processo__arquivar=False,
            autor=cls.superior)
        cls.url = reverse("notifier:oficio_quebra", kwargs={"model_pk": oficio.pk})
        cls.processo = oficio.controlempresasquebra.processo

        super().setUp()


class NotifyOficioFromInterceptacaoTestCase(NotifyTestCaseBase, SetUpTestData, TestCase):

    nome_grupo_superior = 'COORDENADOR DE INTERCEPTAÇÃO/QUEBRA'
    orgao_permission_required = 'access_INTERCEPTACOES'
    view_permission = 'interceptacao.view_interceptacao'
    add_permission = 'interceptacao.add_interceptacao'
    app_template_folder = 'inter'

    def setUp(cls):
        oficio = OfEmpresasInterFactory(
            controlempresasinter__processo__orgao_processo=cls.orgao, controlempresasinter__autor=cls.superior)
        cls.url = reverse("notifier:oficio_inter", kwargs={"model_pk": oficio.pk})
        cls.processo = oficio.controlempresasinter.processo

        super().setUp()


class HowToTelegramViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.profile = ProfileFactory()
        cls.user = cls.profile.user
        cls.user.set_password('django01')
        cls.user.save()

    def setUp(self):
        self.url = reverse('notifier:how_to_telegram')

    def test_notify_nao_logado_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_notify_nao_logado_POST(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_notify_nao_logado_template_used(self):
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, 'componentes/singles/core/Home.html')

    def test_notify_logado(self):
        self.client.login(username=self.user.username, password='django01')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_notify_logado_template_used(self):
        self.client.login(username=self.user.username, password='django01')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'componentes/singles/notifier/InstrucoesTelegram.html')


class AllowTelegramViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.profile = ProfileFactory()
        cls.user = cls.profile.user
        cls.user.set_password('django01')
        cls.user.save()

    def setUp(self):
        TelegramUserFactory(user=self.user, allowed=False)
        self.url = reverse('notifier:allow_telegram')

    def test_notify_nao_logado_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_notify_nao_logado_POST(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_notify_nao_logado_template_used(self):
        response = self.client.get(self.url, follow=True)
        self.assertTemplateUsed(response, 'componentes/singles/core/Home.html')

    def test_notify_logado(self):
        self.client.login(username=self.user.username, password='django01')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_notify_logado_template_used(self):
        self.client.login(username=self.user.username, password='django01')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'componentes/singles/notifier/PermitirNotificacoesTelegram.html')

    def test_allow_notify_logado_template_used(self):
        self.client.login(username=self.user.username, password='django01')
        response = self.client.get(self.url+'?allow=1', follow=True)
        self.assertEqual(TelegramUser.objects.count(), 1)
        self.assertTemplateUsed(response, 'account/notificacoes/notificacoes_recebidas.html')

    def test_unallow_notify_logado_template_used(self):
        self.client.login(username=self.user.username, password='django01')
        response = self.client.get(self.url+'?allow=0', follow=True)
        self.assertEqual(TelegramUser.objects.count(), 0)
        self.assertTemplateUsed(response, 'account/notificacoes/notificacoes_recebidas.html')
