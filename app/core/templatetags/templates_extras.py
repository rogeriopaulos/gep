# -*- coding: utf-8 -*-

from adm.models import Administrativo
from core.models import VinculoProcesso
from dateutil import parser
from django import template
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

register = template.Library()


@register.filter
def tem_permissao(user, permissao):
    return user.has_perm(permissao)


@register.filter
def orgao_tem_permissao(user, permissao_orgao):
    if user.is_superuser:
        return True

    elif user.is_authenticated:
        orgao_obj = user.profile.orgao_link
        return orgao_obj.has_perm(permissao_orgao)

    return False


@register.filter
def is_new_doc(date_creation):
    dt_param = parser.parse(settings.QRCODE_DATE_START)
    dt_start = timezone.make_aware(dt_param)
    return True if date_creation > dt_start else False


@register.filter
def is_same_user(recipient_user, request_user):
    if recipient_user == request_user:
        return 'você'
    else:
        return recipient_user.username


@register.filter
def integra_grupo(user, nome_grupo):
    group = Group.objects.get(name=nome_grupo)
    return True if group in user.groups.all() else False


@register.filter
def get_url(kwarg_url):
    if isinstance(kwarg_url, str):
        url = reverse('adm:detalhe_processo_adm', kwargs={'pk': kwarg_url})
    return url


@register.filter
def get_tipo_procedimento(id):
    adm = Administrativo.objects.filter(pk=id).exists()
    if adm:
        return Administrativo.objects.get(pk=id).get_tipo_procedimento()
    return '-------'


@register.filter
def get_motivo(id_a, id_b):
    vinculo = VinculoProcesso.objects \
        .get(Q(processo_a=id_a, processo_b=id_b) | Q(processo_a=id_b, processo_b=id_a))
    return vinculo.motivo_vinculo
