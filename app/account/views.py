# -*- coding: utf-8 -*-

from adm.models import Administrativo, AtoAdm, OfEmpresas, OficioExternoAdm, OficioInternoAdm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView  # View
from guardian.shortcuts import get_users_with_perms
from notifications.models import Notification
from notifier.helper import NotificationDirectorDisplay, NotificationUserDisplay, NotificationUserSentDisplay

from .forms import ProfileForm, UserForm


@transaction.atomic
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            user.refresh_from_db()
            profile_form = ProfileForm(request.POST, instance=user.profile)
            profile_form.full_clean()
            profile_form.save()
            return redirect('account:register_done')
        else:
            messages.error(request, 'Erro ao criar sua conta')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'account/registro.html', {'user_form': user_form, 'profile_form': profile_form})


class MinhaContaView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):

    template_name = 'account/minha_conta.html'
    success_url = reverse_lazy('account:minha_conta')
    success_message = "Senha alterada com sucesso"

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        if form.user.profile.alterar_senha:
            form.user.profile.alterar_senha = False
            form.user.profile.save()
        return form_valid


minha_conta = MinhaContaView.as_view()


class PasswordResetCustomView(PasswordResetView):

    template_name = 'home.html',
    email_template_name = 'account/password_reset_email.html'
    success_url = reverse_lazy('account:password_reset_done')
    subject_template_name = 'account/password_reset_subject.txt'


class PasswordResetConfirmCustomView(SuccessMessageMixin, PasswordResetConfirmView):

    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('core:home')
    success_message = "Nova senha configurada com sucesso!"


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': dashboard})


class RegisterDoneView(TemplateView):

    template_name = 'account/register_done.html'


class PainelView(LoginRequiredMixin, TemplateView):

    template_name = 'account/painel.html'


painel_view = PainelView.as_view()


@login_required
def processos_criados_json(request):
    user = request.user
    orgao_user = user.profile.orgao_link
    adm = Administrativo.objects.filter(autor=user, orgao_processo=orgao_user)
    procedimentos = [adm]
    data = [processo.to_dict_json() for processos in procedimentos for processo in processos]
    response = {'data': data}
    return JsonResponse(response)


@login_required
def processos_vinculados_json(request):
    user = request.user
    adm = Administrativo.objects.all()
    procedimentos = [adm]
    objs = [processo for processos in procedimentos for processo in processos if user in get_users_with_perms(processo)]
    data = [obj.to_dict_json() for obj in objs]
    response = {'data': data}
    return JsonResponse(response)


@login_required
def atos_json(request):
    user = request.user
    adm = AtoAdm.objects.filter(autor=user)
    procedimentos = [adm]
    data = [processo.to_dict_json() for processos in procedimentos for processo in processos]
    response = {'data': data}
    return JsonResponse(response)


@login_required
def atos_pendentes_json(request):
    user = request.user
    # Ofícios para empresas
    ofemp = OfEmpresas.objects.get_empty_user_files(user)
    # Ofícios internos
    adm_ofinter = OficioInternoAdm.objects.get_empty_user_files(user)
    # Ofício externo
    adm_ofext = OficioExternoAdm.objects.filter(Q(autor=user) & Q(arquivo__exact='') & Q(anulado=False))
    procedimentos = [ofemp, adm_ofinter, adm_ofext]
    data = [ato.to_dict_json() for atos in procedimentos for ato in atos]
    response = {'data': data}
    return JsonResponse(response)


class NotificacoesView(TemplateView):

    template_name = 'account/notificacoes/notificacoes_recebidas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['telegram'] = getattr(user, 'telegramuser', None)
        return context


notificacoes = NotificacoesView.as_view()


@login_required
def notifications_receive_json(request):
    user = request.user
    notifications = user.notifications.all().order_by('-timestamp')

    nt = NotificationUserDisplay(notifications)
    response = {"data": nt.get_notifications_context()}

    return JsonResponse(response)


@login_required
def notificacao_lida(request):
    user = request.user
    nt = user.notifications.get(id=request.GET.get('id'))
    nt.unread = False
    nt.save()
    data = {
        'status': 'success',
        'msg': 'Notificação marcada como lida',
    }
    response = {'data': data}
    return JsonResponse(response)


@login_required
def set_all_notifications_read(request):
    url = reverse('account:notificacoes')

    if request.method == "GET":
        request.user.notifications.filter(unread=True).update(unread=False)
        msg = 'Todas as notificações foram marcadas como lidas.'
        messages.success(request, msg)
    else:
        msg = 'Essa operação não é permitida.'
        messages.error(request, msg)

    return HttpResponseRedirect(url)


class NotificacoesEnviadasView(TemplateView):

    template_name = 'account/notificacoes/notificacoes_enviadas.html'


notifications_sent = NotificacoesEnviadasView.as_view()


@login_required
def notifications_sent_json(request):
    user = request.user
    notifications = Notification.objects.filter(actor_object_id=user.id).order_by('-timestamp')

    nt = NotificationUserSentDisplay(notifications)
    response = {"data": nt.get_notifications_context()}

    return JsonResponse(response)
