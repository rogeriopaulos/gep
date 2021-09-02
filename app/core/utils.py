# -*- coding: utf-8 -*-

from functools import reduce

from guardian.shortcuts import get_objects_for_user, get_users_with_perms
from notifications.signals import notify
from watson.search import get_registered_models


def notify_user(actor, obj, user, verb_text):
    users_with_assignments = get_users_with_perms(obj, attach_perms=True)
    if user not in users_with_assignments:
        notify.send(actor, recipient=[user], verb=verb_text, target=obj)


def deepgetattr(obj, attr):
    """
    Recurses through an attribute chain to get the ultimate value.
    """
    return reduce(getattr, attr.split('.'), obj)


def processos_serializer(user, permission_required, Model):
    orgao = user.profile.orgao_link

    if user.is_superuser:
        processos = Model.objects.all()
        data = [processo.to_dict_json() for processo in processos]
        return {'data': data}

    processos = Model.objects.filter(orgao_processo=orgao)
    data = [processo.to_dict_json() for processo in processos]

    processos_externos = get_objects_for_user(user, permission_required, accept_global_perms=False) \
        .exclude(orgao_processo=orgao)

    data_processos_externos = [
        {**processo.to_dict_json(), **{'processo_externo': True}} for processo in processos_externos
    ]

    response = {'data': data + data_processos_externos}

    return response


class QuerysetWatson:

    gep_modules = {
        'access_ADMINISTRATIVO': 'adm',
    }

    models_filter_params = [
        ['orgao_processo'],
        ['processo', 'orgao_processo'],
        ['controlempresas', 'processo__orgao_processo'],
    ]

    def get_qs_list(self, orgao):
        modules_with_access = self.get_modules_with_access(orgao)
        apps_with_access = [self.gep_modules[key] for key in self.gep_modules if key in modules_with_access]
        qs_list = []

        for model in get_registered_models():
            if model._meta.app_label not in apps_with_access:
                qs_list.append(model.objects.none())
            else:
                qs = self.get_model_qs_by_orgao(model, orgao)
                qs_list.append(qs)

        return qs_list

    def get_modules_with_access(self, orgao):
        return [perm.codename for perm in orgao.permissions.all()]

    def get_model_qs_by_orgao(self, model, orgao):
        for params in self.models_filter_params:
            if hasattr(model, params[0]):
                parameter = '__'.join(params)
                qs = model.objects.filter(**{parameter: orgao})
                return qs

        raise NameError(f'O parâmetro de filtro por orgão não foi definido para o model {model}.')
