# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView, View
from guardian.shortcuts import assign_perm, get_users_with_perms, remove_perm
from guardian.utils import get_40x_or_None
from notifier.tasks import notificar

from .forms import PermUsersFormset, UserExternalMultipleChoiceForm, UserMultipleChoiceForm

GRUPO_SUPERIOR_ADMINISTRATIVO = 'COORDENADORES'
GRUPO_ADMINISTRATIVO = 'USUÁRIOS'
PERMISSOES_ADMINISTRATIVO = [
    'adm.view_administrativo',
    'adm.add_administrativo',
    'adm.change_administrativo'
]


def verifica_direcao(request, subdiretor=None):
    if request.user.groups.filter(name=subdiretor):
        return True
    return False


def padrao_check_permissions(self, request):
    """
    Checks if *request.user* has all permissions returned by
    *get_required_permissions* method.
    :param request: Original request.
    """

    if verifica_direcao(request, self.grupo_superior):
        self.accept_global_perms = True
        request.direcao = True
    obj = self.get_permission_object()
    forbidden = get_40x_or_None(
        request,
        perms=self.get_required_permissions(request),
        obj=obj,
        login_url=self.login_url,
        redirect_field_name=self.redirect_field_name,
        return_403=self.return_403,
        return_404=self.return_404,
        accept_global_perms=self.accept_global_perms
    )
    if forbidden:
        self.on_permission_check_fail(request, forbidden, obj=obj)
    if forbidden and self.raise_exception:
        raise PermissionDenied()
    return forbidden


class SelectUserPermissionView(FormView):
    """
    Classe Pai que permite selecionar os usuários integrantes de um grupo
    específico que, posteriormente, devem ter permissões configuradas em um
    determinado processo.
    """
    template_name = 'componentes/shares/SelectUserPerm.html'
    form_class = UserMultipleChoiceForm

    def get_form_kwargs(self):
        obj = self.get_objeto()
        user_with_perm = get_users_with_perms(obj).values_list('id', flat=True)
        query = User.objects \
            .filter(groups__name=self.name_grupo, is_active=True, profile__orgao_link=obj.orgao_processo) \
            .exclude(id__in=user_with_perm) \
            .order_by('username')
        kwargs = {'queryset': query}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get(self, request, *args, **kwargs):
        if verifica_direcao(request, self.grupo_superior):
            return super(SelectUserPermissionView, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        obj = self.get_objeto()
        users_with_assignments = get_users_with_perms(obj, attach_perms=True)
        actor = self.request.user

        for user in form.cleaned_data['usuarios']:
            for perm in self.permissoes:
                assign_perm(perm, user, obj)

            # notificação automática ao usuário incluído no processo
            if user not in users_with_assignments:

                notification_context = {
                    'actor': serializers.serialize('json', [actor]),
                    'users': serializers.serialize('json', [user]),
                    'verb': 'incluiu',
                    'target': serializers.serialize('json', [obj]),
                    'action_object': serializers.serialize('json', [obj]),
                    'description': 'blog notice'
                }

                notificar.delay(notification_context)

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_objeto()
        context['num_processo'] = obj.numero_processo
        context['modulo'] = self.modulo
        context['usuarios_externos'] = self.usuarios_externos
        return context


class PermissionView(View):

    template_class = 'componentes/shares/PermForUser.html'
    formset_class = PermUsersFormset

    def get(self, request, *args, **kwargs):
        if verifica_direcao(request, self.grupo_superior):
            obj = self.get_objeto()
            users = get_users_with_perms(obj, attach_perms=True)
            initial = []
            for item in users:
                form = {}
                form['username'] = item
                for perm in users[item]:
                    ini_perm = perm.split('_')[0]
                    if ini_perm == 'add':
                        form['adicionar'] = True
                    elif ini_perm == 'change':
                        form['alterar'] = True
                    elif ini_perm == 'view':
                        form['visualizar'] = True
                initial.append(form)
            context = {
                'has_users_with_perm': True if len(users) > 0 else False,
                'formset': self.formset_class(initial=initial),
                'num_processo': obj.numero_processo
            }
            if not context.get('has_users_with_perm'):
                context['processo_url'] = obj.get_absolute_url()
            return render(request, self.template_class, context)
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        formset = self.formset_class(request.POST, request.FILES)

        if formset.is_valid():
            obj = self.get_objeto()
            dados = formset.cleaned_data
            actor = self.request.user

            for item in dados:
                user = User.objects.get(username=item['username'])
                del item['username']

                for campo in item:
                    if campo == 'adicionar':
                        if item[campo]:
                            assign_perm(self.permissoes[1], user, obj)
                        else:
                            remove_perm(self.permissoes[1], user, obj)
                    elif campo == 'alterar':
                        if item[campo]:
                            assign_perm(self.permissoes[2], user, obj)
                        else:
                            remove_perm(self.permissoes[2], user, obj)
                    else:  # Visualizar
                        if item[campo]:
                            assign_perm(self.permissoes[0], user, obj)
                        else:
                            remove_perm(self.permissoes[0], user, obj)

                            notification_context = {
                                'actor': serializers.serialize('json', [actor]),
                                'users': serializers.serialize('json', [user]),
                                'verb': 'removeu',
                                'target': serializers.serialize('json', [obj]),
                                'action_object': serializers.serialize('json', [obj]),
                                'description': 'blog notice'
                            }

                            notificar.delay(notification_context)

        return HttpResponseRedirect(self.get_success_url())


class SelectUserOrgaoExternoView(SelectUserPermissionView):

    form_class = UserExternalMultipleChoiceForm

    def get_form_kwargs(self):
        obj = self.get_objeto()
        user_with_perm = get_users_with_perms(obj).values_list('id', flat=True)
        query = User.objects \
            .filter(groups__name=self.name_grupo, is_active=True) \
            .exclude(Q(id__in=user_with_perm) | Q(profile__orgao_link=obj.orgao_processo)) \
            .order_by('username')
        kwargs = {'queryset': query}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs
