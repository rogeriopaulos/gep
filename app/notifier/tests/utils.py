import adm.tests.factories as adm
from account.tests.factories import OrgaoFactory, ProfileFactory
from django.contrib.auth.models import Group, Permission
from django.test import Client

factories = {
    'adm': (
        adm.AtoAdmFactory,
        adm.DespachoAdmFactory,
        adm.MidiaAdmFactory,
        adm.OficioExternoAdmFactory,
        adm.OficioInternoAdmFactory,
        adm.StatusAdmFactory
    ),
}

adm_class = adm.Administrativo


class SetUpTestData:

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.password = 'Django01'

        cls.orgao = OrgaoFactory()
        orgao_perm = Permission.objects.get(codename=cls.orgao_permission_required)
        cls.orgao.permissions.add(orgao_perm)
        cls.orgao2 = OrgaoFactory()

        profile0 = ProfileFactory(orgao=cls.orgao.orgao, orgao_link=cls.orgao)
        cls.usuario = profile0.user
        cls.usuario.set_password(cls.password)
        cls.usuario.save()

        profile1 = ProfileFactory(orgao=cls.orgao.orgao, orgao_link=cls.orgao)
        cls.normal_user = profile1.user
        cls.normal_user.set_password(cls.password)
        cls.normal_user.save()

        cls.group_superior = Group(name=cls.nome_grupo_superior)
        cls.group_superior.save()

        profile2 = ProfileFactory(orgao=cls.orgao.orgao, orgao_link=cls.orgao)
        cls.superior = profile2.user
        cls.superior.set_password(cls.password)
        cls.superior.save()

        cls.superior.groups.add(cls.group_superior)
