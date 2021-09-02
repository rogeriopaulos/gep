from core.permissions import GRUPO_ADMINISTRATIVO, GRUPO_SUPERIOR_ADMINISTRATIVO
from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):

    help = 'Cria os grupos e permissões exigidos pela aplicação'

    def handle(self, *args, **kwargs):
        self.create_group_manager(GRUPO_SUPERIOR_ADMINISTRATIVO, 'administrativo')
        self.create_group_general(GRUPO_ADMINISTRATIVO, 'administrativo', 'atoadm')

    def create_group_manager(self, group_name, app_name):
        group = Group.objects.create(name=group_name)
        perms = self.get_perms_manager(app_name)
        for perm in perms:
            group.permissions.add(perm)

    def get_perms_manager(self, app_name):
        view = Permission.objects.get(codename=f'view_{app_name}')
        add = Permission.objects.get(codename=f'add_{app_name}')
        change = Permission.objects.get(codename=f'change_{app_name}')
        return [add, change, view]

    def create_group_general(self, group_name, app_name, app_ato_name):
        group = Group.objects.create(name=group_name)
        perms = self.get_perms_general(app_name, app_ato_name)
        for perm in perms:
            group.permissions.add(perm)

    def get_perms_general(self, app_name, app_ato_name):
        view = Permission.objects.get(codename=f'view_{app_name}')
        add = Permission.objects.get(codename=f'add_{app_ato_name}')
        change = Permission.objects.get(codename=f'change_{app_ato_name}')
        return [add, change, view]
