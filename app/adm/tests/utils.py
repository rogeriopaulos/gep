
from account.tests.factories import OrgaoFactory, ProfileFactory
from core.models import AssuntoAdministrativo
from core.tests.factories import AssuntoAdministrativoFactory
from django.contrib.auth.models import Group, Permission
from django.test import Client

assunto_adm = AssuntoAdministrativo.objects.all()
assunto_adm = [assunto.assunto for assunto in assunto_adm]

GRUPO_SUPERIOR_ADMINISTRATIVO = 'COORDENADORES'
GRUPO_ADMINISTRATIVO = 'USUÁRIOS'
PERMISSOES_ADMINISTRATIVO = [
    'view_administrativo',
    'add_administrativo',
    'change_administrativo'
]


class SetUpTestViewsData:

    orgao_permission_required = 'access_ADMINISTRATIVO'

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.password = 'django01'

        cls.orgao = OrgaoFactory()
        orgao_perm = Permission.objects.get(codename=cls.orgao_permission_required)
        cls.orgao.permissions.add(orgao_perm)

        profile0 = ProfileFactory(orgao_link=cls.orgao)
        cls.usuario = profile0.user
        cls.usuario.set_password(cls.password)
        cls.usuario.save()

        profile1 = ProfileFactory(orgao_link=cls.orgao)
        cls.normal_user = profile1.user
        cls.normal_user.set_password(cls.password)
        cls.normal_user.save()

        profile2 = ProfileFactory(orgao_link=cls.orgao)
        cls.superior = profile2.user
        cls.superior.set_password(cls.password)
        cls.superior.save()

        cls.assunto_adm = AssuntoAdministrativoFactory()

        cls.group_superior = Group(name=GRUPO_SUPERIOR_ADMINISTRATIVO)
        cls.group_superior.save()

        cls.superior.groups.add(cls.group_superior)

        cls.group_adm = Group(name=GRUPO_ADMINISTRATIVO)
        cls.group_adm.save()


class SetUpTestDataBase:

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.password = 'Django01'

        cls.orgao = OrgaoFactory()
        orgao_perm = Permission.objects.get(codename='access_ADMINISTRATIVO')
        cls.orgao.permissions.add(orgao_perm)

        profile0 = ProfileFactory(orgao_link=cls.orgao)
        cls.usuario = profile0.user
        cls.usuario.set_password(cls.password)
        cls.usuario.save()

        profile1 = ProfileFactory(orgao_link=cls.orgao)
        cls.normal_user = profile1.user
        cls.normal_user.set_password(cls.password)
        cls.normal_user.save()

        cls.group_superior = Group(name=GRUPO_SUPERIOR_ADMINISTRATIVO)
        cls.group_superior.save()


class SetUpTestViewProcessoData(SetUpTestDataBase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        profile2 = ProfileFactory(orgao_link=cls.orgao)
        cls.superior = profile2.user
        cls.superior.set_password(cls.password)
        cls.superior.save()

        cls.superior.groups.add(cls.group_superior)


class SetUpTestViewAtoData(SetUpTestDataBase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        profile2 = ProfileFactory(orgao_link=cls.orgao)
        cls.superior = profile2.user
        cls.superior.set_password(cls.password)
        cls.superior.save()

        cls.superior.groups.add(cls.group_superior)
