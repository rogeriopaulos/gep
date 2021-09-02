# -*- coding: utf-8 -*-

from core.models import (
    AssuntoAdministrativo,
    ConteudoOficioExterno,
    ConteudoOficioInterno,
    LocalizacaoStatusAdm,
    MotivoVinculo,
    Processo,
    SequenciaDia,
    SequenciaDocumentos,
    TipoGravacao,
    VinculoProcesso
)
from django.contrib import admin
from django.utils.html import mark_safe
from guardian.admin import GuardedModelAdmin


class DocsListFilter(admin.SimpleListFilter):

    title = 'Tem anexo'
    parameter_name = 'tem_anexo'

    def lookups(self, request, model_admin):
        return (
            ('sim', 'Sim'),
            ('não',  'Não'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'sim':
            return queryset.exclude(docs__exact='')
        if self.value() == 'não':
            return queryset.filter(docs__exact='')


class ArquivoListFilter(admin.SimpleListFilter):

    title = 'Tem anexo'
    parameter_name = 'tem_anexo'

    def lookups(self, request, model_admin):

        return (
            ('sim', 'Sim'),
            ('não',  'Não'),
        )

    def queryset(self, request, queryset):

        if self.value() == 'sim':
            return queryset.exclude(arquivo__exact='')

        if self.value() == 'não':
            return queryset.filter(arquivo__exact='')


class ArquivoEmpresasListFilter(admin.SimpleListFilter):

    title = 'Tem anexo'
    parameter_name = 'tem_anexo'

    def lookups(self, request, model_admin):

        return (
            ('sim', 'Sim'),
            ('não',  'Não'),
        )

    def queryset(self, request, queryset):

        if self.value() == 'sim':
            return queryset.exclude(arquivo__exact='', conteudo__exact='')

        if self.value() == 'não':
            return queryset.filter(arquivo__exact='', conteudo__exact='')


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class CoreAdminProced(GuardedModelAdmin):

    date_hierarchy = 'criacao'
    search_fields = ['numero_processo', 'autor__username', 'autor__first_name', 'autor__last_name']
    list_display = ['numero_processo', 'link_processo', 'full_name', 'criacao']
    list_filter = ['criacao', ('arquivar', custom_titled_filter('Processo arquivado'))]
    permission = None

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and request.user.has_perm(self.permission):
            return [f.name for f in self.model._meta.fields]
        return super(CoreAdminProced, self).get_readonly_fields(request, obj=obj)

    def full_name(self, obj):
        return obj.autor.get_full_name().upper()

    full_name.admin_order_field = 'autor'
    full_name.short_description = 'Autor'

    def link_processo(self, obj):
        url = obj.get_absolute_url()
        return mark_safe(f'<a href="{url}" target="_blank">Ver</a>')

    link_processo.short_description = 'Link'
    link_processo.allow_tags = True


class CoreAdminOfEmpresa(admin.ModelAdmin):

    date_hierarchy = 'criacao'
    search_fields = ['autor__username', 'num_oficio', 'autor__first_name', 'autor__last_name']
    list_display = ['get_num_oficio', 'get_operadoras', 'autoridade', 'full_name', 'criacao']
    list_filter = ['autor', 'criacao', 'confirmacao', ArquivoEmpresasListFilter]
    permission = None

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and request.user.has_perm(self.permission):
            return [f.name for f in self.model._meta.fields]
        return super(CoreAdminOfEmpresa, self).get_readonly_fields(request, obj=obj)

    def get_num_oficio(self, obj):
        return obj.num_oficio

    get_num_oficio.admin_order_field = 'num_oficio'
    get_num_oficio.short_description = 'Número'

    def full_name(self, obj):
        return obj.autor.get_full_name()

    full_name.admin_order_field = 'autor'
    full_name.short_description = 'Autor'

    def get_operadoras(self, obj):
        if obj.empresa == '21':
            return obj.outros
        else:
            return obj.get_empresa_display()

    get_operadoras.admin_order_field = 'empresa'
    get_operadoras.short_description = 'Empresa'


class CoreAdminDespacho(admin.ModelAdmin):

    date_hierarchy = 'criacao'
    search_fields = ['processo__numero_processo', 'autor__username', 'autor__first_name', 'autor__last_name', ]
    list_display = ['full_name', 'get_processo', 'criacao']
    list_filter = ['autor', 'criacao']
    permission = None

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and request.user.has_perm(self.permission):
            return [f.name for f in self.model._meta.fields]
        return super(CoreAdminDespacho, self).get_readonly_fields(request, obj=obj)

    def get_processo(self, obj):
        url = obj.processo.get_absolute_url()
        num = obj.processo.numero_processo
        return mark_safe(f'<a href="{url}" target="_blank">{num}</a>')

    get_processo.admin_order_field = 'processo__numero_processo'
    get_processo.short_description = 'Processo'
    get_processo.allow_tags = True

    def full_name(self, obj):
        return obj.autor.get_full_name()

    full_name.admin_order_field = 'autor'
    full_name.short_description = 'Autor'


class CoreAdminOfInterno(admin.ModelAdmin):

    date_hierarchy = 'criacao'
    search_fields = ['processo__numero_processo', 'autor__username',
                     'autor__first_name', 'autor__last_name', 'destino', 'num_oficio']
    list_display = ('get_num_oficio', 'destino', 'get_processo', 'full_name', 'criacao', 'get_doc')
    list_filter = ('autor', 'criacao', 'confirmacao', ArquivoListFilter)
    permission = None

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and request.user.has_perm(self.permission):
            return [f.name for f in self.model._meta.fields]
        return super(CoreAdminOfInterno, self).get_readonly_fields(request, obj=obj)

    def get_num_oficio(self, obj):
        return obj.num_oficio

    get_num_oficio.admin_order_field = 'num_oficio'
    get_num_oficio.short_description = 'Número'

    def get_processo(self, obj):
        url = obj.processo.get_absolute_url()
        num = obj.processo.numero_processo
        return mark_safe(f'<a href="{url}" target="_blank">{num}</a>')

    get_processo.admin_order_field = 'processo__numero_processo'
    get_processo.short_description = 'Processo'
    get_processo.allow_tags = True

    def full_name(self, obj):
        return obj.autor.get_full_name()

    full_name.admin_order_field = 'autor'
    full_name.short_description = 'Autor'

    def get_doc(self, obj):
        doc = obj.arquivo
        if doc:
            return mark_safe(f'<a href="{obj.arquivo.url}" target="_blank">Download</a>')
        return 'sem anexo'

    get_doc.short_description = 'Anexo'
    get_doc.allow_tags = True


class CoreAdminOfExterno(admin.ModelAdmin):

    date_hierarchy = 'criacao'
    search_fields = ['processo__numero_processo', 'autor__username',
                     'autor__first_name', 'autor__last_name', 'origem', 'num_oficio']
    list_display = ('get_num_oficio', 'origem', 'get_processo', 'full_name', 'criacao', 'get_doc')
    list_filter = ('autor', 'criacao', 'data_recebimento', ArquivoListFilter)
    permission = None

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and request.user.has_perm(self.permission):
            return [f.name for f in self.model._meta.fields]
        return super(CoreAdminOfExterno, self).get_readonly_fields(request, obj=obj)

    def get_num_oficio(self, obj):
        return obj.num_oficio

    get_num_oficio.admin_order_field = 'num_oficio'
    get_num_oficio.short_description = 'Número'

    def get_processo(self, obj):
        url = obj.processo.get_absolute_url()
        num = obj.processo.numero_processo
        return mark_safe(f'<a href="{url}" target="_blank">{num}</a>')

    get_processo.admin_order_field = 'processo__numero_processo'
    get_processo.short_description = 'Processo'
    get_processo.allow_tags = True

    def full_name(self, obj):
        return obj.autor.get_full_name()

    full_name.admin_order_field = 'autor'
    full_name.short_description = 'Autor'

    def get_doc(self, obj):
        doc = obj.arquivo
        if doc:
            return mark_safe(f'<a href="{obj.arquivo.url}" target="_blank">Download</a>')
        return 'sem anexo'

    get_doc.short_description = 'Anexo'
    get_doc.allow_tags = True


class CoreAdminMidia(admin.ModelAdmin):

    date_hierarchy = 'criacao'
    search_fields = [
        'processo__numero_processo', 'autor__username', 'autor__first_name',
        'autor__last_name', 'destino', 'solicitante', 'num_midia'
    ]
    list_display = ('get_num_midia', 'tipo_gravacao_link', 'get_processo', 'full_name', 'criacao', 'get_doc')
    list_filter = ('autor', 'criacao', ArquivoListFilter)
    permission = None

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and request.user.has_perm(self.permission):
            return [f.name for f in self.model._meta.fields]
        return super(CoreAdminMidia, self).get_readonly_fields(request, obj=obj)

    def get_num_midia(self, obj):
        return obj.num_midia

    get_num_midia.admin_order_field = 'num_midia'
    get_num_midia.short_description = 'Número'

    def get_processo(self, obj):
        url = obj.processo.get_absolute_url()
        num = obj.processo.numero_processo
        return mark_safe(f'<a href="{url}" target="_blank">{num}</a>')

    get_processo.admin_order_field = 'processo__numero_processo'
    get_processo.short_description = 'Processo'
    get_processo.allow_tags = True

    def full_name(self, obj):
        return obj.autor.get_full_name()

    full_name.admin_order_field = 'autor'
    full_name.short_description = 'Autor'

    def get_doc(self, obj):
        doc = obj.docs
        if doc:
            return mark_safe(f'<a href="{obj.docs.url}" target="_blank">Download</a>')
        return 'sem anexo'

    get_doc.short_description = 'Anexo'
    get_doc.allow_tags = True


class SequenciaDiaAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'sequencia', 'criacao')
    ordering = ('-criacao',)


admin.site.register(SequenciaDia, SequenciaDiaAdmin)


class SequenciaDocumentosAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'sequencia', 'tipo', 'orgao', 'get_orgao_sigla', 'criacao')
    ordering = ('-criacao',)

    def get_orgao_sigla(self, obj):
        return obj.orgao.sigla

    get_orgao_sigla.short_description = 'Sigla do órgão'


admin.site.register(SequenciaDocumentos, SequenciaDocumentosAdmin)


admin.site.register(AssuntoAdministrativo)
admin.site.register(ConteudoOficioExterno)
admin.site.register(ConteudoOficioInterno)
admin.site.register(LocalizacaoStatusAdm)
admin.site.register(MotivoVinculo)
admin.site.register(Processo)
admin.site.register(TipoGravacao)
admin.site.register(VinculoProcesso)
