# -*- coding: utf-8 -*-

from account.models import Profile
from adm.models import OfEmpresas
from ajax_datatable.views import AjaxDatatableView
from core.forms import VinculoProcessoForm
from core.models import Processo, VinculoProcesso
from core.permissions import verifica_direcao
from core.utils import QuerysetWatson, deepgetattr
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, TemplateView
from guardian.shortcuts import get_objects_for_user
from watson import search as watson
from watson.views import SearchApiView, SearchView


class HomeView(TemplateView):

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['account/painel.html']

        return ['componentes/singles/core/Home.html']


home_view = HomeView.as_view()


class DnispCoreArquivoUpdateMixin(LoginRequiredMixin):

    fields = ['docs']
    template_name = 'componentes/shares/PopupDnisp.html'

    def get_queryset(self):
        queryset = super(DnispCoreArquivoUpdateMixin, self).get_queryset()
        queryset = queryset.filter(autor=self.request.user)
        return queryset

    def form_valid(self, form):
        form.instance.modificador = self.request.user
        self.object = form.save()
        return super(DnispCoreArquivoUpdateMixin, self).form_valid(form)


class DespachoMixin():

    template_name = 'componentes/shares/CKEditorConteudo.html'

    def get_context_data(self, **kwargs):
        context = super(DespachoMixin, self).get_context_data(**kwargs)
        context['subtitle'] = self.subtitle
        context['path_to_include'] = self.path_to_include
        return context


class GerarOfEmpresasMixin():

    template_name = 'componentes/shares/CKEditorConteudo.html'

    def get_context_data(self, **kwargs):
        context = super(GerarOfEmpresasMixin, self).get_context_data(**kwargs)
        context['subtitle'] = self.subtitle
        context['path_to_include'] = self.path_to_include
        return context


class ProrrogacaoMixin():

    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(ProrrogacaoMixin, self).get_context_data(**kwargs)
        context['subtitle'] = "Cadastrar Prorrogação"
        return context


class GravacaoMidiaMixin():

    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(GravacaoMidiaMixin, self).get_context_data(**kwargs)
        context['subtitle'] = "Adicionar Gravação de Mídia"
        return context


class OfExternoMixin():

    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(OfExternoMixin, self).get_context_data(**kwargs)
        context['subtitle'] = self.subtitle
        context['outros_disabled'] = True
        return context


class OfInternoMixin():

    template_name = 'componentes/shares/FormGeral.html'
    of_interno_update = False

    def get_context_data(self, **kwargs):
        context = super(OfInternoMixin, self).get_context_data(**kwargs)
        context['subtitle'] = self.subtitle
        context['outros_disabled'] = self.outros_disabled
        context['processos_css'] = self.processos_css
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        processo = None
        if self.of_interno_update:
            return kwargs
        else:
            processo = get_object_or_404(self.processo_class, pk=self.kwargs['pk'])
        kwargs['orgao_pk'] = processo.orgao_processo.pk
        return kwargs


class VigiaMixin():

    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(VigiaMixin, self).get_context_data(**kwargs)
        context['subtitle'] = self.subtitle
        context['vigia_form'] = True
        return context


class AutoCircunstanciadoMixin():

    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(AutoCircunstanciadoMixin, self).get_context_data(**kwargs)
        context['subtitle'] = "Adicionar Auto Circunstanciado"
        return context


class RelintMixin():

    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(RelintMixin, self).get_context_data(**kwargs)
        context['subtitle'] = "Adicionar Relatório de Inteligência"
        return context


class PedidoBuscaMixin():

    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(PedidoBuscaMixin, self).get_context_data(**kwargs)
        context['subtitle'] = "Pedido de Busca"
        return context


class RetecMixin():

    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(RetecMixin, self).get_context_data(**kwargs)
        context['subtitle'] = "Adicionar Relatório Técnico"
        return context


class RelInternoMixin():

    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(RelInternoMixin, self).get_context_data(**kwargs)
        context['subtitle'] = "Adicionar Relatório Interno"
        return context


class OrdemBuscaMixin():

    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(OrdemBuscaMixin, self).get_context_data(**kwargs)
        context['subtitle'] = "Adicionar Ordem de Busca"
        return context


class RelBuscaMixin():

    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(RelBuscaMixin, self).get_context_data(**kwargs)
        context['subtitle'] = "Relatório de Busca"
        return context


class OrgaoPermissionRequiredMixin(AccessMixin):

    ato_update_view = False
    ato_create_view = False
    processo_model = None

    def get_object_processo(self, queryset=None):
        """
        Retorna o objeto Processo que a View está mostrando.
        """
        if getattr(self, "get_objeto", None):
            return self.get_objeto()

        if queryset is None:
            queryset = self.get_queryset()

        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        if pk is None and slug is None:
            return None
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': queryset.model._meta.verbose_name})

        if not isinstance(obj, Processo):
            return None

        return obj

    def get_view_permission_object(self, perm_name):

        perm_obj = None
        if '.' in perm_name:
            app_label, codename = perm_name.split('.')
            perm_obj = get_object_or_404(Permission, codename=codename, content_type__app_label=app_label)
        else:
            perm_obj = get_object_or_404(Permission, codename=perm_name)

        return perm_obj

    def user_orgao_has_perm(self, request, processo_permission, orgao_permission, processo_obj=None):
        profile = get_object_or_404(Profile, user=request.user)
        orgao = profile.orgao_link
        orgao_perm_obj = self.get_view_permission_object(orgao_permission)

        if request.user.is_superuser:
            return True

        if processo_obj and processo_permission and request.user.has_perm(processo_permission, processo_obj):
            return True

        if processo_obj and processo_obj.orgao_processo != orgao:
            return False

        if orgao_perm_obj in orgao.permissions.all():
            return True

        return False

    def dispatch(self, request, *args, **kwargs):
        obj = None

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if self.ato_create_view and self.processo_model:
            obj = get_object_or_404(self.processo_model, pk=self.kwargs['pk'])
        elif self.ato_update_view:
            ato_obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
            ato_attrs = {
                OfEmpresas: 'controlempresas.processo',
            }
            attr = ato_attrs.get(ato_obj.__class__, 'processo')
            obj = deepgetattr(ato_obj, attr)

        else:
            obj = self.get_object_processo()

        processo_permission = None
        if hasattr(self, 'view_permission_required'):
            processo_permission = self.view_permission_required
        elif hasattr(self, 'permission_required'):
            processo_permission = self.permission_required

        orgao_permission = self.orgao_permission_required

        orgao_has_perm = self.user_orgao_has_perm(
            self.request, processo_permission=processo_permission, orgao_permission=orgao_permission, processo_obj=obj)

        if not orgao_has_perm:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class VincularProcessosCreateMixin(LoginRequiredMixin, OrgaoPermissionRequiredMixin, CreateView):

    model = VinculoProcesso
    form_class = VinculoProcessoForm
    template_name = 'componentes/shares/VincularProcessos.html'
    model_dispatch = None
    group_dispatch = ''

    def get_object_processo(self):
        return get_object_or_404(self.model_dispatch, pk=self.kwargs['pk'])

    def dispatch(self, request, *args, **kwargs):
        objeto = get_object_or_404(self.model_dispatch, pk=self.kwargs['pk'])
        if verifica_direcao(request, self.group_dispatch):
            if objeto.arquivar is False:
                return super(VincularProcessosCreateMixin, self).dispatch(request, *args, **kwargs)
            else:
                return redirect('core:arquivado')
        else:
            raise PermissionDenied

    def form_valid(self, form):
        form.instance.autor = self.request.user
        processo_a = Processo.objects.get(pk=self.kwargs['pk'])
        if processo_a.id == form.cleaned_data['processo_b'].id:
            messages.warning(self.request, 'Não é possível vincular um processo com ele mesmo')
            return redirect(self.get_success_url())
        form.instance.processo_a = processo_a
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        processo = None

        processo = get_object_or_404(self.model_dispatch, pk=self.kwargs['pk'])
        kwargs['orgao_pk'] = processo.orgao_processo.pk
        return kwargs


class ProcessosAjaxDatatableView(AjaxDatatableView):

    def get_permission_object(self, perm_name):

        perm_obj = None
        if '.' in perm_name:
            app_label, codename = perm_name.split('.')
            perm_obj = get_object_or_404(Permission, codename=codename, content_type__app_label=app_label)
        else:
            perm_obj = get_object_or_404(Permission, codename=perm_name)

        return perm_obj

    def user_orgao_has_perm(self, user, orgao_permission):
        orgao = user.profile.orgao_link
        orgao_perm_obj = self.get_permission_object(orgao_permission)

        if user.is_superuser:
            return True

        if orgao_perm_obj in orgao.permissions.all():
            return True

        return False

    def get_qs_by_orgao(self, request):
        user = request.user
        orgao = user.profile.orgao_link

        if user.is_superuser:
            return self.model.objects.all()

        processos = self.model.objects.filter(orgao_processo=orgao)
        processos_externos = get_objects_for_user(
            user,
            self.processo_permission_required,
            accept_global_perms=False,
            any_perm=True
        ).exclude(orgao_processo=orgao)

        return processos | processos_externos

    def get_initial_queryset(self, request=None):
        if not request.user.is_authenticated:
            raise PermissionDenied

        elif not self.user_orgao_has_perm(request.user, self.orgao_permission_required):
            raise PermissionDenied

        return self.get_qs_by_orgao(request)


class ProcessosListView(LoginRequiredMixin, OrgaoPermissionRequiredMixin, TemplateView):

    template_name = 'componentes/shares/ProcessosList.html'

    def get_object_processo(self, queryset=None):
        return None

    def get_context_data(self, **kwargs):
        context = super(ProcessosListView, self).get_context_data(**kwargs)
        context['url_cadastrar'] = self.url_cadastrar
        context['url_processos_ajax'] = self.url_processos_ajax
        return context


class OrgaoPermRequiredWithoutObjMixin(OrgaoPermissionRequiredMixin):

    def get_object_processo(self, queryset=None):
        return None


class BuscasGEPMixin:

    def get_queryset(self):
        orgao = self.request.user.profile.orgao_link
        qs_watson = QuerysetWatson()
        qs_list = qs_watson.get_qs_list(orgao)

        return watson.search(self.query, models=qs_list, exclude=self.get_exclude())

    def get(self, request, *args, **kwargs):
        """Performs a GET request."""
        self.query = self.get_query(request)
        if not self.query:
            empty_query_redirect = self.get_empty_query_redirect()
            if empty_query_redirect:
                return redirect(empty_query_redirect)
        return super().get(request, *args, **kwargs)


class BuscaMultiOrgaosView(LoginRequiredMixin, BuscasGEPMixin, SearchView):

    context_object_name = 'resultados'
    template_name = 'componentes/singles/buscas/_ResultadoBusca.html'
    paginate_by = 20


busca_multi_orgaos = BuscaMultiOrgaosView.as_view()


class BuscaMultiOrgaosApiView(LoginRequiredMixin, BuscasGEPMixin, SearchApiView):

    pass


busca_multi_orgaos_api = BuscaMultiOrgaosApiView.as_view()
