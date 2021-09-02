# -*- coding: utf-8 -*-

from core.permissions import (
    GRUPO_ADMINISTRATIVO,
    GRUPO_SUPERIOR_ADMINISTRATIVO,
    PERMISSOES_ADMINISTRATIVO,
    PermissionView,
    SelectUserOrgaoExternoView,
    SelectUserPermissionView,
    padrao_check_permissions,
    verifica_direcao
)
from core.validators import ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from core.views import (
    DespachoMixin,
    GravacaoMidiaMixin,
    OfExternoMixin,
    OfInternoMixin,
    OrgaoPermissionRequiredMixin,
    ProcessosAjaxDatatableView,
    ProcessosListView,
    VincularProcessosCreateMixin
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, UpdateView
from easy_pdf.views import PDFTemplateResponseMixin
from guardian.mixins import PermissionRequiredMixin

from .forms import (
    AdministrativoForm,
    AdministrativoUpdateForm,
    ControlEmpresasForm,
    DespachoAdmForm,
    DocumentoAdmForm,
    MidiaAdmForm,
    OfEmpresasFormset,
    OfEmpresasUpdateForm,
    OficioExternoAdmForm,
    OficioInternoAdmForm,
    OfInternoAdmUpdateForm,
    StatusAdmForm
)
from .models import (
    Administrativo,
    AtoAdm,
    ControlEmpresas,
    DespachoAdm,
    DocumentosGeraisAdm,
    MidiaAdm,
    OfEmpresas,
    OficioExternoAdm,
    OficioInternoAdm,
    StatusAdm
)


class AdministrativoCreateView(LoginRequiredMixin, OrgaoPermissionRequiredMixin, SuccessMessageMixin, CreateView):

    model = Administrativo
    form_class = AdministrativoForm
    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    view_permission_required = 'adm.add_administrativo'
    template_name = 'componentes/shares/FormsCriarProcedimento.html'
    success_message = "Procedimento criado com sucesso"

    def get(self, request, *args, **kwargs):
        user_has_perm = self.request.user.has_perm(self.view_permission_required)
        user_has_authority = verifica_direcao(request, GRUPO_SUPERIOR_ADMINISTRATIVO)
        if user_has_perm or user_has_authority:
            return super(AdministrativoCreateView, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(AdministrativoCreateView, self).get_context_data(**kwargs)
        context['title_header'] = 'Cadastrar Processo'
        context['form_adm'] = True
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.autor = user
        form.instance.orgao_processo = user.profile.orgao_link
        form.instance.gerar_numero_processo()
        return super(AdministrativoCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('adm:detalhe_processo_adm', kwargs={'pk': self.object.pk})


criar_processo_adm = AdministrativoCreateView.as_view()


class AdministrativoUpdateView(LoginRequiredMixin, OrgaoPermissionRequiredMixin, SuccessMessageMixin, UpdateView):

    model = Administrativo
    form_class = AdministrativoUpdateForm
    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    view_permission_required = 'adm.change_administrativo'
    template_name = 'componentes/shares/FormsCriarProcedimento.html'
    success_message = "Procedimento atualizado com sucesso"

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Administrativo, pk=self.kwargs['pk'])
        user_has_perm = self.request.user.has_perm(self.view_permission_required, obj)
        user_has_authority = verifica_direcao(request, GRUPO_SUPERIOR_ADMINISTRATIVO)
        if user_has_perm or user_has_authority:
            return super(AdministrativoUpdateView, self).get(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(AdministrativoUpdateView, self).get_context_data(**kwargs)
        context['title_header'] = 'Editar Processo'
        context['form_adm'] = True
        return context

    def form_valid(self, form):
        arquivar = form.cleaned_data.get('arquivar')
        with transaction.atomic():
            if arquivar is True:
                form.instance.arquivador = self.request.user
                form.instance.data_arquivamento = timezone.now()
            form.instance.modificador = self.request.user
        return super(AdministrativoUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('adm:detalhe_processo_adm', kwargs={'pk': self.object.pk})


editar_processo_adm = AdministrativoUpdateView.as_view()


class AdministrativoListView(ProcessosListView):

    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    view_permission_required = 'adm.view_administrativo'
    url_cadastrar = reverse_lazy('adm:criar_processo_adm')
    url_processos_ajax = reverse_lazy('adm:processos_adm_ajax')


listar_adm = AdministrativoListView.as_view()


class AdministrativoAjaxDatatableView(ProcessosAjaxDatatableView):

    model = Administrativo
    title = 'Administrativo'
    initial_order = [["criacao", "desc"], ]
    search_values_separator = '+'
    show_column_filters = False
    length_menu = [[25, 50, 100, 300], [25, 50, 100, 300]]
    processo_permission_required = ['adm.view_administrativo', 'adm.add_administrativo', 'adm.change_administrativo']
    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    disable_queryset_optimization = True

    column_defs = [
        ProcessosAjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, 'searchable': False, 'orderable': False},
        {'name': 'observacao', 'visible': False, 'searchable': True},
        {'name': 'criacao', 'title': 'Criação'},
        {'name': 'numero_processo', 'title': 'Processo'},
        {'name': 'oficiante', },
        {'name': 'destino_adm', 'max_length': 40},
        {
            'name': 'assunto_adm',
            'title': 'Assunto',
            'foreign_field': 'assunto_adm__assunto',
            'max_length': 40
        },
        {'name': 'outro', 'visible': False, 'searchable': True},
        {'name': 'sigla', 'title': 'Criado por', 'foreign_field': 'orgao_processo__sigla'},
        {
            'name': 'acessar',
            'title': ('<i class="glyphicon glyphicon-link" data-toggle="tooltip" '
                      + 'data-placement="bottom" title="Link"></i>'),
            'searchable': False,
            'orderable': False,
            'className': 'text-center'
        },
    ]

    def customize_row(self, row, obj):
        processo_externo = ' processo-externo' if obj.orgao_processo != self.request.user.profile.orgao_link else ''
        arquivado = ' arquivado' if obj.arquivar else ''
        row['acessar'] = f"""
            <a href='{obj.get_absolute_url()}'
             class='btn btn-primary btn-xs{arquivado}{processo_externo}' role='button'>
               <strong>Ver Processo <i class="glyphicon glyphicon-share-alt"></i>
            </a>
            """
        row['assunto_adm'] = obj.get_assunto()

    def render_row_details(self, pk, request=None):

        obj = self.model.objects.get(pk=pk)

        return f"""
            <div class='row' style='margin-left: 5px'>
            <div>
                <p><strong>Observação: </strong> {obj.observacao}</p>
            </div>
            </div>
        """


processos_adm_ajax = AdministrativoAjaxDatatableView.as_view()


class AdministrativoDetailView(PermissionRequiredMixin, OrgaoPermissionRequiredMixin, DetailView):

    model = Administrativo
    context_object_name = 'processo_adm'
    template_name = 'componentes/singles/processos/adm/detalhes/_DetalheGeral.html'
    permission_required = 'adm.view_administrativo'
    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    raise_exception = True
    grupo_superior = GRUPO_SUPERIOR_ADMINISTRATIVO

    def get_context_data(self, **kwargs):
        context = super(AdministrativoDetailView, self).get_context_data(**kwargs)
        context['atos'] = self.object.get_all_atos()
        context['is_coordenador'] = verifica_direcao(self.request, GRUPO_SUPERIOR_ADMINISTRATIVO)
        context['anulacao_baseurl'] = reverse('adm:anular_ato', kwargs={'pk': '0'})
        return context

    def check_permissions(self, request):
        padrao_check_permissions(self, request)


detalhe_processo_adm = AdministrativoDetailView.as_view()


class AdmExtratoPdfView(PDFTemplateResponseMixin, LoginRequiredMixin, OrgaoPermissionRequiredMixin, DetailView):

    model = Administrativo
    template_name = 'componentes/singles/processos/adm/ExtratoPdf.html'
    context_object_name = 'processo_adm'
    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    view_permission_required = 'adm.view_administrativo'

    def get_context_data(self, **kwargs):
        context = super(AdmExtratoPdfView, self).get_context_data(**kwargs)
        context['atos'] = self.object.get_all_atos()
        return context


extrato_pdf_adm = AdmExtratoPdfView.as_view()


class AtoAdmCreateView(LoginRequiredMixin, OrgaoPermissionRequiredMixin, CreateView):

    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    view_permission_required = 'adm.add_administrativo'
    ato_create_view = True
    processo_model = Administrativo

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Administrativo, pk=self.kwargs['pk'])
        user_has_perm = self.request.user.has_perm(self.view_permission_required, obj)
        user_has_authority = verifica_direcao(request, GRUPO_SUPERIOR_ADMINISTRATIVO)
        if user_has_perm or user_has_authority:
            if obj.arquivar is False:
                return super(AtoAdmCreateView, self).get(request, *args, **kwargs)
            else:
                return redirect('core:arquivado')
        else:
            raise PermissionDenied

    def set_instance_form(self, form):
        form.instance.autor = self.request.user
        form.instance.processo = Administrativo.objects.get(pk=self.kwargs['pk'])
        form.instance.tipo_ato = self.kwargs['tipo_ato']

    def get_success_url(self):
        return reverse_lazy('notifier:ato_adm', kwargs={'model_pk': self.object.pk})


class AtoAdmUpdateView(OrgaoPermissionRequiredMixin, UpdateView):

    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    view_permission_required = 'adm.change_administrativo'
    ato_update_view = True

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        user_has_perm = self.request.user.has_perm(self.view_permission_required, obj.processo)
        user_has_authority = verifica_direcao(request, GRUPO_SUPERIOR_ADMINISTRATIVO)
        if user_has_perm or user_has_authority:
            if obj.processo.arquivar is False:
                return super(AtoAdmUpdateView, self).get(request, *args, **kwargs)
            else:
                return redirect('core:arquivado')
        else:
            raise PermissionDenied


class OfInternoCreateView(OfInternoMixin, AtoAdmCreateView):

    model = OficioInternoAdm
    form_class = OficioInternoAdmForm
    processo_class = Administrativo
    outros_disabled = True
    subtitle = 'Expedir Ofício'
    processos_css = False

    def form_valid(self, form):
        self.set_instance_form(form)
        return super(OfInternoCreateView, self).form_valid(form)


add_ofinterno_adm = OfInternoCreateView.as_view()


class OfInternoUpdateView(LoginRequiredMixin, OfInternoMixin, AtoAdmUpdateView):

    model = OficioInternoAdm
    form_class = OfInternoAdmUpdateForm
    processo_class = Administrativo
    of_interno_update = True
    outros_disabled = False
    subtitle = 'Modificar Ofício Expedido'
    processos_css = True

    def form_valid(self, form):
        data = {x: valor for x, valor in form.cleaned_data.items()
                if valor is not None and valor is not False and valor != ''}
        data['modificador'] = self.request.user
        data['autoridade'] = str(data['autoridade'])
        OficioInternoAdm.objects.filter(pk=self.kwargs['pk']).update(**data)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('notifier:ato_adm', kwargs={'model_pk': self.object.pk})


editar_ofinterno_adm = OfInternoUpdateView.as_view()


class OfInternoArquivoUpdateView(LoginRequiredMixin, AtoAdmUpdateView):

    model = OficioInternoAdm
    fields = ['arquivo']
    template_name = 'componentes/shares/DadosPopup.html'

    def get_context_data(self, **kwargs):
        context = super(OfInternoArquivoUpdateView, self).get_context_data(**kwargs)
        context['max_size'] = MAX_FILE_SIZE
        context['allowed_extensions'] = ALLOWED_EXTENSIONS
        return context

    def form_valid(self, form):
        form.instance.modificador = self.request.user
        self.object = form.save()
        return super(OfInternoArquivoUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('notifier:ato_adm', kwargs={'model_pk': self.object.pk})


editar_ofinterno_arq_adm = OfInternoArquivoUpdateView.as_view()


class OfInternoAdmConfirmView(LoginRequiredMixin, AtoAdmUpdateView):

    model = OficioInternoAdm
    fields = ['confirmacao', 'nome_confirm']
    template_name = 'componentes/shares/ConfirmacaoPopup.html'

    def form_valid(self, form):
        form.instance.modificador = self.request.user
        return super(OfInternoAdmConfirmView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('notifier:ato_adm', kwargs={'model_pk': self.object.pk})


editar_confirmacao_adm = OfInternoAdmConfirmView.as_view()


class OfInternoAdmDataEnvioView(LoginRequiredMixin, AtoAdmUpdateView):

    model = OficioInternoAdm
    fields = ['data_envio']
    template_name = 'componentes/shares/DataEnvioPopup.html'

    def form_valid(self, form):
        form.instance.modificador = self.request.user
        self.object = form.save()
        return super(OfInternoAdmDataEnvioView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('notifier:ato_adm', kwargs={'model_pk': self.object.pk})


editar_dataenvio_adm = OfInternoAdmDataEnvioView.as_view()


class OfExternoAdmCreateView(OfExternoMixin, AtoAdmCreateView):

    model = OficioExternoAdm
    form_class = OficioExternoAdmForm
    subtitle = "Adicionar Ofício Recebido"

    def form_valid(self, form):
        self.set_instance_form(form)
        return super(OfExternoAdmCreateView, self).form_valid(form)


add_ofexterno_adm = OfExternoAdmCreateView.as_view()


class OfExternoAdmUpdateView(LoginRequiredMixin, OfExternoMixin, AtoAdmUpdateView):

    model = OficioExternoAdm
    form_class = OficioExternoAdmForm
    subtitle = "Modificar Ofício Recebido"

    def form_valid(self, form):
        data = {x: valor for x, valor in form.cleaned_data.items()
                if valor is not None and valor is not False and valor != ''}
        data['modificador'] = self.request.user
        OficioExternoAdm.objects.filter(pk=self.kwargs['pk']).update(**data)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('notifier:ato_adm', kwargs={'model_pk': self.object.pk})


editar_ofexterno_adm = OfExternoAdmUpdateView.as_view()


class DespachoAdmCreateView(DespachoMixin, AtoAdmCreateView):

    model = DespachoAdm
    form_class = DespachoAdmForm
    path_to_include = 'componentes/shares/CKDespachoGeral.html'
    subtitle = 'Cadastrar Despacho'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Administrativo, pk=self.kwargs['pk'])
        if verifica_direcao(request, GRUPO_SUPERIOR_ADMINISTRATIVO):
            if obj.arquivar is False:
                return super(DespachoAdmCreateView, self).get(request, *args, **kwargs)
            else:
                return redirect('core:arquivado')
        else:
            raise PermissionDenied

    def form_valid(self, form):
        self.set_instance_form(form)
        return super(DespachoAdmCreateView, self).form_valid(form)


add_despacho_adm = DespachoAdmCreateView.as_view()


class DespachoAdmUpdateView(LoginRequiredMixin, DespachoMixin, AtoAdmUpdateView):

    model = DespachoAdm
    form_class = DespachoAdmForm
    path_to_include = 'componentes/shares/CKDespachoEditar.html'
    subtitle = 'Editar Despacho'

    def get_queryset(self):
        queryset = super(DespachoAdmUpdateView, self).get_queryset()
        queryset = queryset.filter(autor=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('notifier:ato_adm', kwargs={'model_pk': self.object.pk})

    def form_valid(self, form):
        form.instance.modificador = self.request.user
        return super(DespachoAdmUpdateView, self).form_valid(form)


editar_despacho_adm = DespachoAdmUpdateView.as_view()


class StatusAdmCreateView(AtoAdmCreateView):

    model = StatusAdm
    form_class = StatusAdmForm
    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(StatusAdmCreateView, self).get_context_data(**kwargs)
        context['subtitle'] = 'Inserir Status'
        context['outros_disabled'] = True
        return context

    def form_valid(self, form):
        self.set_instance_form(form)
        return super(StatusAdmCreateView, self).form_valid(form)


add_status_adm = StatusAdmCreateView.as_view()


class StatusAdmUpdateView(LoginRequiredMixin, AtoAdmUpdateView):

    model = StatusAdm
    form_class = StatusAdmForm
    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(StatusAdmUpdateView, self).get_context_data(**kwargs)
        context['subtitle'] = 'Inserir Status'
        context['outros_disabled'] = True
        return context

    def form_valid(self, form):
        form.instance.modificador = self.request.user
        return super(StatusAdmUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('notifier:ato_adm', kwargs={'model_pk': self.object.pk})


editar_status_adm = StatusAdmUpdateView.as_view()


class GravacaoAdmCreateView(GravacaoMidiaMixin, AtoAdmCreateView):

    model = MidiaAdm
    form_class = MidiaAdmForm

    def form_valid(self, form):
        self.set_instance_form(form)
        return super(GravacaoAdmCreateView, self).form_valid(form)


add_gravacao_adm = GravacaoAdmCreateView.as_view()


class DocumentoCreateView(AtoAdmCreateView):

    model = DocumentosGeraisAdm
    form_class = DocumentoAdmForm
    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(DocumentoCreateView, self).get_context_data(**kwargs)
        context['subtitle'] = 'Adicionar Documento'
        context['outros_disabled'] = True
        return context

    def form_valid(self, form):
        self.set_instance_form(form)
        return super(DocumentoCreateView, self).form_valid(form)


add_documento_adm = DocumentoCreateView.as_view()


class DocumentoUpdateView(LoginRequiredMixin, AtoAdmUpdateView):

    model = DocumentosGeraisAdm
    form_class = DocumentoAdmForm
    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        context = super(DocumentoUpdateView, self).get_context_data(**kwargs)
        context['subtitle'] = 'Atualizar Documento-SSP/PI'
        return context

    def get_queryset(self):
        queryset = super(DocumentoUpdateView, self).get_queryset()
        queryset = queryset.filter(autor=self.request.user)
        return queryset

    def form_valid(self, form):
        data = {x: valor for x, valor in form.cleaned_data.items()
                if valor is not None and valor is not False and valor != ''}
        data['modificador'] = self.request.user
        self.model.objects.filter(pk=self.kwargs['pk']).update(**data)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('notifier:ato_adm', kwargs={'model_pk': self.object.pk})


editar_documento_adm = DocumentoUpdateView.as_view()


class SelectUserPermissionAdmView(LoginRequiredMixin, OrgaoPermissionRequiredMixin, SelectUserPermissionView):

    permissoes = PERMISSOES_ADMINISTRATIVO
    model = Administrativo
    name_grupo = GRUPO_ADMINISTRATIVO
    grupo_superior = GRUPO_SUPERIOR_ADMINISTRATIVO
    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    view_permission_required = 'adm.view_administrativo'
    modulo = 'Administrativo'
    usuarios_externos = False

    def get_objeto(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('adm:select_perm_adm', kwargs={'pk': self.kwargs['pk']})


select_user_adm = SelectUserPermissionAdmView.as_view()


class SelectUserOrgaoExternoAdmView(LoginRequiredMixin, OrgaoPermissionRequiredMixin, SelectUserOrgaoExternoView):

    permissoes = PERMISSOES_ADMINISTRATIVO
    model = Administrativo
    name_grupo = GRUPO_ADMINISTRATIVO
    grupo_superior = GRUPO_SUPERIOR_ADMINISTRATIVO
    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    view_permission_required = 'adm.view_administrativo'
    modulo = 'Administrativo'
    usuarios_externos = True

    def get_objeto(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('adm:select_perm_adm', kwargs={'pk': self.kwargs['pk']})


add_external_users_adm = SelectUserOrgaoExternoAdmView.as_view()


class PermissionAdmView(LoginRequiredMixin, OrgaoPermissionRequiredMixin, PermissionView):

    model = Administrativo
    permissoes = PERMISSOES_ADMINISTRATIVO
    grupo_superior = GRUPO_SUPERIOR_ADMINISTRATIVO
    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    view_permission_required = 'adm.view_administrativo'

    def get_objeto(self):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('adm:detalhe_processo_adm', kwargs={'pk': self.kwargs['pk']})


select_perm_adm = PermissionAdmView.as_view()


class AnularAtoView(LoginRequiredMixin, OrgaoPermissionRequiredMixin, UpdateView):

    model = AtoAdm
    fields = ['motivo_anulacao']
    pk_url_kwarg = 'pk'
    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    view_permission_required = 'adm.view_administrativo'

    def get_object_processo(self):
        ato = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return ato.processo

    def dispatch(self, request, *args, **kwargs):
        objeto = get_object_or_404(self.model, pk=self.kwargs['pk'])
        if verifica_direcao(request, GRUPO_SUPERIOR_ADMINISTRATIVO):
            if objeto.processo.arquivar is False:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('core:arquivado')
        else:
            raise PermissionDenied

    def form_valid(self, form):
        if form.cleaned_data['motivo_anulacao'] == '':
            messages.warning(self.request, 'Informe um motivo ao anular um ato')
            return redirect(self.get_success_url())
        self.object.anulado = True
        self.object.modificador = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('adm:detalhe_processo_adm', kwargs={'pk': self.object.processo.pk})


anular_ato = AnularAtoView.as_view()


class VincularProcessosCreateView(VincularProcessosCreateMixin):

    model_dispatch = Administrativo
    group_dispatch = GRUPO_SUPERIOR_ADMINISTRATIVO
    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    view_permission_required = 'adm.view_administrativo'

    def get_success_url(self):
        obj = get_object_or_404(Administrativo, pk=self.kwargs['pk'])
        return reverse_lazy('adm:detalhe_processo_adm', kwargs={'pk': obj.pk})


vincular_processos = VincularProcessosCreateView.as_view()


class ControlEmpresasCreateView(AtoAdmCreateView):

    model = ControlEmpresas
    form_class = ControlEmpresasForm
    template_name = 'componentes/shares/OficioEmpresas.html'

    def get_context_data(self, **kwargs):
        data = super(ControlEmpresasCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['oficios'] = OfEmpresasFormset(self.request.POST, form_kwargs=self.get_formset_kwargs())
        else:
            data['oficios'] = OfEmpresasFormset(form_kwargs=self.get_formset_kwargs())
        data['oficios_inter'] = True
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        oficios = context['oficios']
        with transaction.atomic():
            self.set_instance_form(form)
            self.object = form.save()
            if oficios.is_valid():
                oficios.instance = self.object
                oficios.save()
        return super(ControlEmpresasCreateView, self).form_valid(form)

    def get_formset_kwargs(self):
        processo = get_object_or_404(Administrativo, pk=self.kwargs['pk'])
        return {'orgao_pk': processo.orgao_processo.pk}


add_ofempresas = ControlEmpresasCreateView.as_view()


class OfEmpresaUpdateViewMixin(OrgaoPermissionRequiredMixin, UpdateView):

    orgao_permission_required = 'account.access_ADMINISTRATIVO'
    view_permission_required = 'adm.change_administrativo'
    ato_update_view = True

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        user_has_perm = self.request.user.has_perm(self.view_permission_required, obj.controlempresas.processo)
        user_has_authority = verifica_direcao(request, GRUPO_SUPERIOR_ADMINISTRATIVO)
        if user_has_perm or user_has_authority:
            if obj.controlempresas.processo.arquivar is False:
                return super(OfEmpresaUpdateViewMixin, self).get(request, *args, **kwargs)
            else:
                return redirect('core:arquivado')
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse_lazy('adm:detalhe_processo_adm', kwargs={'pk': self.object.controlempresas.processo.pk})


class OfEmpresasArquivoUpdateView(LoginRequiredMixin, OfEmpresaUpdateViewMixin):

    model = OfEmpresas
    fields = ['arquivo']
    template_name = 'componentes/shares/DadosPopup.html'

    def get_context_data(self, **kwargs):
        context = super(OfEmpresasArquivoUpdateView, self).get_context_data(**kwargs)
        context['max_size'] = MAX_FILE_SIZE
        context['allowed_extensions'] = ALLOWED_EXTENSIONS
        return context

    def form_valid(self, form):
        form.instance.modificador = self.request.user
        return super(OfEmpresasArquivoUpdateView, self).form_valid(form)


ofempresas_upload_arquivo = OfEmpresasArquivoUpdateView.as_view()


class OfEmpresaConfirmUpdateView(LoginRequiredMixin, OfEmpresaUpdateViewMixin):

    model = OfEmpresas
    fields = ['confirmacao', 'nome_confirm']
    template_name = 'componentes/shares/ConfirmacaoPopup.html'

    def form_valid(self, form):
        form.instance.modificador = self.request.user
        return super(OfEmpresaConfirmUpdateView, self).form_valid(form)


ofempresas_confirmar = OfEmpresaConfirmUpdateView.as_view()


class OfEmpresasUpdateView(LoginRequiredMixin, OfEmpresaUpdateViewMixin):

    model = OfEmpresas
    form_class = OfEmpresasUpdateForm
    template_name = 'componentes/shares/FormGeral.html'

    def get_context_data(self, **kwargs):
        data = super(OfEmpresasUpdateView, self).get_context_data(**kwargs)
        data['processos_css'] = True
        data['subtitle'] = 'Atualizar Ofício'
        return data

    def form_valid(self, form):
        form.instance.modificador = self.request.user
        return super(StatusAdmUpdateView, self).form_valid(form)


ofempresas_editar = OfEmpresasUpdateView.as_view()
