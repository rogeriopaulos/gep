import adm.models as adm
import core
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from guardian.shortcuts import get_users_with_perms

from .forms import NotifiedUsersForm
from .tasks import notificar
from .utils import atos


class NotifierView(LoginRequiredMixin, FormView):

    template_name = 'componentes/shares/NotifyForm.html'
    form_class = NotifiedUsersForm

    verb = 'notificou'

    def dispatch(self, request, *args, **kwargs):
        if hasattr(self, 'settings'):
            self.settings(self, request, *args, **kwargs)
        return super(NotifierView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.check_permission()
        self.notify_users(form)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(NotifierView, self).get_context_data(**kwargs)
        context['obj'] = self.obj
        context['success_url'] = self.success_url
        return context

    def get_form(self, form_class=None):
        self.check_permission()
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(queryset=self.notificados(), **self.get_form_kwargs())

    def check_permission(self):
        user_has_perm = self.request.user in get_users_with_perms(self.processo)
        user_has_authority = self.request.user.groups.filter(name=self.GRUPO_SUPERIOR)
        user_at_orgao = self.request.user.profile.orgao_link == self.processo.orgao_processo

        if user_has_authority and not (user_at_orgao or user_has_perm):
            raise PermissionDenied

        if not user_has_authority and not user_has_perm:
            raise PermissionDenied

    def notificados(self):
        users_with_perms = get_users_with_perms(self.processo)
        authorities = User.objects \
            .filter((Q(groups__name=self.GRUPO_SUPERIOR)) & Q(profile__orgao_link=self.processo.orgao_processo)) \
            .distinct()
        users = users_with_perms | authorities
        return users.filter(is_superuser__exact=False, is_active__exact=True).order_by('first_name')

    def notify_users(self, form):
        actor = self.request.user
        users = form.cleaned_data['usuarios']
        notification_context = {
            'actor': serializers.serialize('json', [actor]),
            'users': serializers.serialize('json', users),
            'verb': self.verb,
            'target': serializers.serialize('json', [self.processo]),
            'action_object': serializers.serialize('json', [self.obj]),
            'description': self.processo.get_absolute_url()
        }
        notificar.delay(notification_context)

    def settings(self, request, *args, **kwargs):
        self.set_obj(self, request, *args, **kwargs)
        self.set_processo(self, request, *args, **kwargs)
        self.set_success_url(self, request, *args, **kwargs)

    def set_obj(self, request, *args, **kwargs):
        self.obj = get_object_or_404(self.model, pk=self.kwargs['model_pk'])

    def set_processo(self, request, *args, **kwargs):
        self.processo = self.obj.processo

    def set_success_url(self, request, *args, **kwargs):
        self.success_url = self.obj.processo.get_absolute_url()


class NotifyAtoAdmView(NotifierView):

    GRUPO_SUPERIOR = core.permissions.GRUPO_SUPERIOR_ADMINISTRATIVO
    model = adm.AtoAdm
    submodels = atos['adm']

    def set_obj(self, request, *args, **kwargs):
        super().set_obj(request)
        self.obj = self.submodels[self.obj.tipo_ato].objects.get(pk=self.obj.pk)


notifica_ato_adm = NotifyAtoAdmView.as_view()


class NotifyOficioEmpresaView(NotifierView):

    GRUPO_SUPERIOR = core.permissions.GRUPO_SUPERIOR_ADMINISTRATIVO
    model = adm.OfEmpresas

    def set_processo(self, request, *args, **kwargs):
        self.processo = self.obj.controlempresas.processo

    def set_success_url(self, request, *args, **kwargs):
        self.success_url = self.obj.controlempresas.processo.get_absolute_url()


notifica_oficio_empresa = NotifyOficioEmpresaView.as_view()
