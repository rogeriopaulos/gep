from datetime import date

from adm.tests.factories import (
    AdministrativoFactory,
    DespachoAdmFactory,
    DocumentoAdmFactory,
    MidiaAdmFactory,
    OficioExternoAdmFactory,
    OficioInternoAdmFactory,
    StatusAdmFactory
)
from core.tests.factories import AssuntoAdministrativoFactory, MotivoVinculo, VinculoProcesso
from django.test import TestCase
from django.urls import reverse


class AdministrativoTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.processo = AdministrativoFactory()

    def test_get_notification_label(self):
        resultado_esperado = f'Processo nº {self.processo.numero_processo}'
        self.assertEqual(self.processo.get_notification_label(), resultado_esperado)

    def test_str(self):
        resultado_esperado = str(self.processo)
        self.assertEqual(resultado_esperado, self.processo.numero_processo)

    def test_get_absolute_url(self):
        resultado_esperado = reverse('adm:detalhe_processo_adm', kwargs={'pk': self.processo.id})
        self.assertEqual(self.processo.get_absolute_url(), resultado_esperado)

    def test_get_processos_vinculados(self):
        processo_b = AdministrativoFactory()
        processo_c = AdministrativoFactory()
        motivo = MotivoVinculo.objects.create(motivo='Um motivo qualquer.')
        VinculoProcesso.objects.create(
            autor=self.processo.autor,
            processo_a=self.processo,
            processo_b=processo_b,
            motivo_vinculo=motivo
        )
        VinculoProcesso.objects.create(
            autor=self.processo.autor,
            processo_a=processo_c,
            processo_b=self.processo,
            motivo_vinculo=motivo
        )

        self.assertTrue(self.processo.get_processos_vinculados())

    def test_get_assunto(self):
        resultado_esperado = self.processo.assunto_adm.assunto
        self.assertEqual(self.processo.get_assunto(), resultado_esperado)

    def test_get_assunto_outro(self):
        resultado_esperado = self.processo.outro.upper()
        self.processo.assunto_adm = AssuntoAdministrativoFactory(assunto='OUTRO(S)')
        self.assertEqual(self.processo.get_assunto(), resultado_esperado)

    def test_to_dict_json(self):
        resultado_esperado = {
            'criacao': self.processo.criacao.strftime('%d/%m/%Y'),
            'processo': self.processo.numero_processo,
            'oficiante': self.processo.oficiante,
            'destino': self.processo.destino_adm,
            'assunto': self.processo.get_assunto(),
            'link': self.processo.get_absolute_url(),
            'observacao': self.processo.observacao,
            'arquivado': self.processo.arquivar,
            'tipo': self.processo.get_tipo_procedimento()
        }
        self.assertEqual(self.processo.to_dict_json(), resultado_esperado)


class OficioInternoAdmTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.processo = AdministrativoFactory()
        cls.oficio_interno = OficioInternoAdmFactory(
            processo=cls.processo,
            autor=cls.processo.autor,
            autoridade=cls.processo.autor
        )

    def test_get_titulo(self):
        resultado_esperado = f'Processo nº {self.processo.numero_processo}'
        self.assertEqual(
            self.oficio_interno.get_titulo(),
            resultado_esperado)

    def test_str(self):
        resultado_esperado = f'Ofício nº {self.oficio_interno.num_oficio}'
        self.assertEqual(str(self.oficio_interno), resultado_esperado)

    def test_get_absolute_url(self):
        resultado_esperado = reverse('adm:detalhe_processo_adm', kwargs={'pk': self.processo.id})
        self.assertEqual(self.oficio_interno.get_absolute_url(), resultado_esperado)

    def test_get_ato_label(self):
        label = {
            '1': 'OFÍCIO EXPEDIDO',
            '2': 'OFÍCIO RECEBIDO',
            '3': 'DESPACHO',
            '4': 'STATUS',
            '5': 'GRAVAÇÃO DE MÍDIA',
            '6': 'OFÍCIO GABINETE - SSP-PI',
        }

        self.assertEqual(self.oficio_interno.get_ato_label(), label[str(self.oficio_interno.tipo_ato)])

    def test_to_dict_json(self):
        resultado_esperado = {
            'ato': self.oficio_interno.__str__().upper(),
            'numero': self.oficio_interno.processo.numero_processo,
            'nome': None,
            'tipo': self.oficio_interno.processo.get_tipo_procedimento(),
            'criacao': self.oficio_interno.criacao.strftime('%d/%m/%Y'),
            'link': self.oficio_interno.processo.get_absolute_url(),
        }
        self.assertEqual(self.oficio_interno.to_dict_json(), resultado_esperado)


class OficioExternoAdmTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.processo = AdministrativoFactory()
        cls.oficio_externo = OficioExternoAdmFactory(
            processo=cls.processo, autor=cls.processo.autor)

    def test_str(self):
        resultado_esperado = f'Ofício nº {self.oficio_externo.num_oficio}'
        self.assertEqual(str(self.oficio_externo), resultado_esperado)

    def test_get_absolute_url(self):
        resultado_esperado = reverse('adm:detalhe_processo_adm', kwargs={'pk': self.processo.id})
        self.assertEqual(self.oficio_externo.get_absolute_url(), resultado_esperado)

    def test_get_procedimento(self):
        resultado_esperado = self.processo.numero_processo
        self.assertEqual(self.oficio_externo.get_procedimento(), resultado_esperado)

    def test_get_titulo(self):
        resultado_esperado = f'Processo nº {self.oficio_externo.processo.numero_processo}'
        self.assertEqual(self.oficio_externo.get_titulo(), resultado_esperado)

    def test_get_tipo_procedimento(self):
        resultado_esperado = 'Administrativo - Ofício Recebido'
        self.assertEqual(self.oficio_externo.get_tipo_procedimento(), resultado_esperado)


class DespachoAdmTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.processo = AdministrativoFactory()
        cls.despacho = DespachoAdmFactory(processo=cls.processo, autor=cls.processo.autor)

    def test_str(self):
        resultado_esperado = f'Despacho - {self.despacho.criacao.strftime("%d/%m/%Y")}'
        self.assertEqual(str(self.despacho), resultado_esperado)

    def test_to_dict_json(self):
        resultado_esperado = {
            'ato': str(self.despacho).upper(),
            'numero': self.despacho.processo.numero_processo,
            'nome': None,
            'tipo': 'Administrativo',
            'criacao': self.despacho.criacao.strftime('%d/%m/%Y'),
            'link': f'/processos/{self.despacho.processo.pk}/detalhes/'
        }
        self.assertEqual(self.despacho.to_dict_json(), resultado_esperado)

    def test_count_obj_by_years(self):
        current_year = date.today().year
        resultado_esperado = {year: 0 for year in range(2018, current_year+1)}
        resultado_esperado[current_year] += 1
        self.assertEqual(self.despacho.count_obj_by_years(), resultado_esperado)


class StatusAdmTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.processo = AdministrativoFactory()
        cls.status_adm = StatusAdmFactory(processo=cls.processo, autor=cls.processo.autor)

    def test_str(self):
        resultado_esperado = f'Status - Processo {self.status_adm.processo.numero_processo} / '
        resultado_esperado += f'{self.status_adm.local} - {self.status_adm.situacao}'
        self.assertEqual(str(self.status_adm), resultado_esperado)

    def test_get_titulo(self):
        resultado_esperado = self.status_adm.situacao
        self.assertEqual(self.status_adm.get_titulo(), resultado_esperado)


class MidiaAdmTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.processo = AdministrativoFactory()
        cls.midia_adm = MidiaAdmFactory(
            processo=cls.processo, autor=cls.processo.autor)

    def test_str(self):
        resultado_esperado = f'Mídia nº: {self.midia_adm.num_midia} - {self.midia_adm.tipo_gravacao_link}'
        self.assertEqual(str(self.midia_adm), resultado_esperado)

    def test_get_absolute_url(self):
        resultado_esperado = reverse('adm:detalhe_processo_adm', kwargs={'pk': self.processo.id})
        self.assertEqual(self.midia_adm.get_absolute_url(), resultado_esperado)

    def test_get_procedimento(self):
        resultado_esperado = self.processo.numero_processo
        self.assertEqual(self.midia_adm.get_procedimento(), resultado_esperado)

    def test_get_origem(self):
        resultado_esperado = self.processo.oficiante
        self.assertEqual(self.midia_adm.get_origem(), resultado_esperado)

    def test_get_tipo_procedimento(self):
        resultado_esperado = 'Administrativo - Mídia'
        self.assertEqual(self.midia_adm.get_tipo_procedimento(), resultado_esperado)


class DocumentoAdmTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.processo = AdministrativoFactory()
        cls.documento = DocumentoAdmFactory(
            processo=cls.processo, autor=cls.processo.autor)

    def test_str(self):
        resultado_esperado = f'Documentos Gerais: {self.documento.nome_doc}'
        self.assertEquals(str(self.documento), resultado_esperado)

    def test_get_tipo_procedimento(self):
        resultado_esperado = 'Administrativo - Documentos Gerais'
        self.assertEquals(self.documento.get_tipo_procedimento(), resultado_esperado)

    def test_get_procedimento(self):
        resultado_esperado = self.processo.administrativo.numero_processo
        self.assertEquals(self.documento.get_procedimento(), resultado_esperado)

    def test_get_origem(self):
        resultado_esperado = self.processo.administrativo.oficiante
        self.assertEquals(self.documento.get_origem(), resultado_esperado)

    def test_get_titulo(self):
        resultado_esperado = 'Processo nº {}'.format(self.documento.processo.administrativo.numero_processo)
        self.assertEquals(self.documento.get_titulo(), resultado_esperado)

    def test_get_criacao(self):
        resultado_esperado = self.documento.criacao.strftime('%d/%m/%Y')
        self.assertEquals(self.documento.get_criacao(), resultado_esperado)
