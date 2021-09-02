# -*- coding: utf-8 -*-

from django.apps import AppConfig
from watson import search as watson


class AdmConfig(AppConfig):

    name = 'adm'
    verbose_name = 'GEP | Administrativo'

    def ready(self):
        # ------------------------- ADMINISTRATIVO ------------------------- #
        Administrativo = self.get_model("Administrativo")
        watson.register(
            Administrativo,
            AdministrativoSearchAdapter,
            store=('get_destino', 'get_origem', 'get_tipo_procedimento',)
        )

        OficioInternoAdm = self.get_model('OficioInternoAdm')
        watson.register(
            OficioInternoAdm,
            OficioInternoAdmSearchAdapter,
            store=('get_procedimento', 'get_criacao', 'get_origem', 'get_tipo_procedimento', 'get_titulo',)
        )

        DocumentosGeraisAdm = self.get_model('DocumentosGeraisAdm')
        watson.register(
            DocumentosGeraisAdm,
            DocumentosGeraisAdmSearchAdapter,
            store=('get_procedimento', 'get_criacao', 'get_origem', 'get_tipo_procedimento', 'get_titulo',
                   'nome_doc', 'descricao')
        )

        OficioExternoAdm = self.get_model('OficioExternoAdm')
        watson.register(
            OficioExternoAdm,
            OficioExternoAdmSearchAdapter,
            store=('get_procedimento', 'get_criacao', 'get_origem', 'get_tipo_procedimento', 'get_titulo',)
        )

        MidiaAdm = self.get_model("MidiaAdm")
        watson.register(
            MidiaAdm,
            MidiaAdmSearchAdapter,
            store=('get_titulo', 'get_origem', 'get_procedimento', 'get_tipo_procedimento', 'get_criacao',)
        )

        OfEmpresas = self.get_model("OfEmpresas")
        watson.register(
            OfEmpresas,
            OfEmpresasSearchAdapter,
            store=('get_titulo', 'get_origem', 'get_procedimento', 'get_tipo_procedimento', 'get_criacao',)
        )


class AdministrativoSearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        num = obj.administrativo.numero_processo
        title = 'Administrativo - Processo nº {}'.format(num)
        return title


class OficioInternoAdmSearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        return 'Ofício nº {}'.format(obj.num_oficio)


class OficioExternoAdmSearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        return 'Ofício nº {}'.format(obj.num_oficio)


class MidiaAdmSearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        return 'Mídia nº {}'.format(obj.num_midia)


class DocumentosGeraisAdmSearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        return 'Documentos Gerais: {}'.format(obj.nome_doc)

    def get_descricao(self, obj):
        return 'Descricao {}'.format(obj.descricao)


class OfEmpresasSearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        return f'Ofício nº {obj.num_oficio} - {obj.get_empresa_display()}'
