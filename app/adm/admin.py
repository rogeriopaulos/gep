# -*- coding: utf-8 -*-

from core.admin import (
    CoreAdminDespacho,
    CoreAdminMidia,
    CoreAdminOfEmpresa,
    CoreAdminOfExterno,
    CoreAdminOfInterno,
    CoreAdminProced
)
from django.contrib import admin
from django.utils.html import mark_safe

from .models import (
    Administrativo,
    DespachoAdm,
    DocumentosGeraisAdm,
    MidiaAdm,
    OfEmpresas,
    OficioExternoAdm,
    OficioInternoAdm
)


class AdministrativoAdmin(CoreAdminProced):

    search_fields = CoreAdminProced.search_fields + ['assunto_adm', 'outro', 'destino_adm', 'oficiante']
    list_display = CoreAdminProced.list_display + ['get_assunto', 'destino_adm', 'oficiante']
    list_filter = CoreAdminProced.list_filter + ['assunto_adm']
    permission = 'adm.view_administrativo'

    def get_assunto(self, obj):
        if obj.assunto_adm == 'OUTRO(S)':
            return obj.outro
        return obj.assunto_adm

    get_assunto.admin_order_field = 'assunto_adm'
    get_assunto.short_description = 'Conteúdo'


admin.site.register(Administrativo, AdministrativoAdmin)


class DespachoAdmAdmin(CoreAdminDespacho):

    permission = 'adm.view_ato'


admin.site.register(DespachoAdm, DespachoAdmAdmin)


class OfInternoAdmAdmin(CoreAdminOfInterno):

    permission = 'adm.view_ato'


admin.site.register(OficioInternoAdm, OfInternoAdmAdmin)


class OfExternoAdmAdmin(CoreAdminOfExterno):

    permission = 'adm.view_ato'


admin.site.register(OficioExternoAdm, OfExternoAdmAdmin)


class MidiaAdmAdmin(CoreAdminMidia):

    permission = 'adm.view_ato'


admin.site.register(MidiaAdm, MidiaAdmAdmin)


class DocumentoAdmAdmin(admin.ModelAdmin):

    date_hierarchy = 'criacao'
    list_display = ('nome_doc', 'get_processo', 'full_name', 'criacao', 'get_doc', 'anulado')

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
        doc = obj.documento
        if doc:
            return mark_safe(f'<a href="{doc.url}" target="_blank">Download</a>')
        return 'sem anexo'

    get_doc.short_description = 'Anexo'
    get_doc.allow_tags = True


admin.site.register(DocumentosGeraisAdm, DocumentoAdmAdmin)


class OfEmpresasAdmin(CoreAdminOfEmpresa):

    list_display = CoreAdminOfEmpresa.list_display + ['get_processo', 'get_doc']
    permission = 'adm.view_ato'

    def get_processo(self, obj):
        url = obj.controlempresas.processo.get_absolute_url()
        num = obj.controlempresas.processo.numero_processo
        return mark_safe(f'<a href="{url}" target="_blank">{num}</a>')

    processo = 'controlempresas__processo__numero_processo'
    get_processo.admin_order_field = processo
    get_processo.short_description = 'Processo'
    get_processo.allow_tags = True

    def get_doc(self, obj):
        if obj.arquivo:
            return mark_safe(f'<a href="{obj.arquivo.url}" target="_blank">Download</a>')
        elif obj.conteudo:
            url = obj.controlempresas.processo.get_absolute_url()
            num = obj.controlempresas.processo.numero_processo
            return mark_safe(f'<a href="{url}" target="_blank">{num}</a>')
        else:
            return 'sem anexo'

    get_doc.short_description = 'Anexo'
    get_doc.allow_tags = True


admin.site.register(OfEmpresas, OfEmpresasAdmin)
