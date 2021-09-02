# -*- coding: utf-8 -*-

from auditlog.registry import auditlog
from core.managers import OfEmpresasManager, OfInternoManager
from core.models import (
    AssuntoAdministrativo,
    CamposComuns,
    Despacho,
    Documento,
    LocalizacaoStatusAdm,
    Midia,
    OficioEmpresas,
    OficioExterno,
    OfInterno,
    Processo,
    VinculoProcesso,
    gerar_numero_documento
)
from core.validators import file_validator
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone


class Administrativo(Processo):

    assunto_adm = models.ForeignKey(
        AssuntoAdministrativo,
        on_delete=models.CASCADE,
        related_name='processos_adm',
        verbose_name='Conteúdo principal',
        null=True
    )
    outro = models.CharField('Outro(s)', max_length=140, blank=True)
    destino_adm = models.CharField('Destinatário', max_length=255, blank=True)
    oficiante = models.CharField('Órgão/autoridade oficiante', max_length=255, blank=True)
    email = models.EmailField('Email de contato do oficiante', blank=True)
    fone = models.CharField('Fone de contato do oficiante', max_length=15, blank=True)
    observacao = models.TextField('Observação', blank=True)
    arquivo = models.FileField(verbose_name='Documento', upload_to='administrativo/inicial/%Y/%m/%d/', blank=True)

    class Meta:
        verbose_name = 'ADMINISTRATIVO - Processo'
        verbose_name_plural = 'ADMINISTRATIVO - Processos'

    def __str__(self):
        return self.numero_processo

    def get_absolute_url(self):
        return reverse('adm:detalhe_processo_adm', kwargs={'pk': self.pk})

    def get_all_atos(self):
        return AtoAdm.objects \
            .select_related(
                'despachoadm',
                'midiaadm',
                'oficioexternoadm',
                'oficiointernoadm',
                'statusadm',
                'documentosgeraisadm'
            ) \
            .filter(processo__pk=self.pk) \
            .order_by('-criacao')

    def get_url_addofinterno(self):
        return reverse('adm:add_ofinterno_adm', kwargs={'pk': self.pk, 'tipo_ato': '1'})

    def get_url_addofexterno(self):
        return reverse('adm:add_ofexterno_adm', kwargs={'pk': self.pk, 'tipo_ato': '2'})

    def get_url_adddespacho(self):
        return reverse('adm:add_despacho_adm', kwargs={'pk': self.pk, 'tipo_ato': '3'})

    def get_url_addstatus(self):
        return reverse('adm:add_status_adm', kwargs={'pk': self.pk, 'tipo_ato': '4'})

    def get_url_addmidia(self):
        return reverse('adm:add_gravacao_adm', kwargs={'pk': self.pk, 'tipo_ato': '5'})

    def get_url_adddocumento(self):
        return reverse('adm:add_documento_adm', kwargs={'pk': self.pk, 'tipo_ato': '6'})

    def get_url_addofempresas(self):
        return reverse('adm:add_ofempresas', kwargs={'pk': self.pk, 'tipo_ato': '7'})

    def get_destino(self):
        return self.destino_adm

    def get_origem(self):
        return self.oficiante

    def get_tipo_procedimento(self):
        return 'Administrativo'

    def get_url_selecionausers(self):
        return reverse('adm:select_user_adm', kwargs={'pk': self.pk})

    def get_url_add_external_users(self):
        return reverse('adm:add_external_users_adm', kwargs={'pk': self.pk})

    def get_url_defineperm(self):
        return reverse('adm:select_perm_adm', kwargs={'pk': self.pk})

    def get_notification_label(self):
        return 'Processo nº {}'.format(self.numero_processo)

    def get_processos_vinculados(self):
        qs = VinculoProcesso.objects.filter(Q(processo_a=self) | Q(processo_b=self))
        objs = []
        for i in qs:
            if i.processo_a.id == self.id:
                objs.append(i.processo_b)
            elif i.processo_b.id == self.id:
                objs.append(i.processo_a)
        return objs

    def get_assunto(self):
        if self.assunto_adm.assunto.upper() == 'OUTRO(S)':
            return self.outro.upper()
        return self.assunto_adm.assunto

    def to_dict_json(self):
        return {
            'criacao': timezone.localtime(self.criacao).strftime('%d/%m/%Y'),
            'processo': self.numero_processo,
            'oficiante': self.oficiante,
            'destino': self.destino_adm,
            'assunto': self.get_assunto(),
            'link': self.get_absolute_url(),
            'observacao': self.observacao,
            'arquivado': self.arquivar,
            'tipo': self.get_tipo_procedimento()
        }


class AtoAdm(CamposComuns):

    processo = models.ForeignKey(
        'Administrativo',
        on_delete=models.CASCADE,
        verbose_name='Processo',
        related_name='processo'
    )
    TIPO_ATO = (
        ('1', 'OFÍCIO INTERNO'),
        ('2', 'OFÍCIO EXTERNO'),
        ('3', 'DESPACHO'),
        ('4', 'STATUS'),
        ('5', 'GRAVAÇÃO DE MÍDIA'),
        ('6', 'DOCUMENTO'),
        ('7', 'OFÍCIOS PARA EMPRESAS'),
    )
    tipo_ato = models.CharField('Tipo de Ato', max_length=2, choices=TIPO_ATO)
    descricao = models.TextField('Observação', blank=True)
    anulado = models.BooleanField('Anular ato', default=False)
    motivo_anulacao = models.TextField('Motivo da anulação', blank=True)

    class Meta:
        verbose_name = "Administrativo - Ato"
        verbose_name_plural = "Administrativo - Atos"

    def __str__(self):
        return '{}'.format(self.get_tipo_ato_display())

    def to_dict_json(self):
        return {
            'ato': self.__str__().upper(),
            'numero': self.processo.numero_processo,
            'nome': None,
            'tipo': self.processo.get_tipo_procedimento(),
            'criacao': timezone.localtime(self.criacao).strftime('%d/%m/%Y'),
            'link': self.processo.get_absolute_url(),
        }

    def get_ato_label(self):
        label = {
            '1': 'OFÍCIO EXPEDIDO',
            '2': 'OFÍCIO RECEBIDO',
            '3': 'DESPACHO',
            '4': 'STATUS',
            '5': 'GRAVAÇÃO DE MÍDIA',
            '6': 'DOCUMENTOS GERAIS',
            '7': 'OFÍCIOS PARA EMPRESAS',
        }
        return label[str(self.tipo_ato)]


class OficioInternoAdm(AtoAdm, OfInterno):

    arquivo = models.FileField(
        verbose_name='Arquivo',
        upload_to='administrativo/oficios_internos/%Y/%m/%d/',
        blank=True,
        validators=[file_validator()]
    )

    objects = OfInternoManager()

    class Meta:
        verbose_name = "ADMINISTRATIVO - Ofício Interno"
        verbose_name_plural = "ADMINISTRATIVO - Ofícios Internos"
        permissions = (('view_ato', 'Pode ver esse ato'),)

    def __str__(self):
        return 'Ofício nº {}'.format(self.num_oficio)

    def get_absolute_url(self):
        return reverse('adm:detalhe_processo_adm', kwargs={'pk': self.processo.administrativo.pk})

    def get_tipo_procedimento(self):
        return 'Administrativo - Ofício Expedido'

    def get_procedimento(self):
        return self.processo.administrativo.numero_processo

    def get_origem(self):
        return self.processo.administrativo.oficiante

    def get_titulo(self):
        return 'Processo nº {}'.format(self.processo.administrativo.numero_processo)

    def get_criacao(self):
        return timezone.localdate(self.criacao).strftime('%d/%m/%Y')


class OficioExternoAdm(AtoAdm, OficioExterno):

    arquivo = models.FileField(
        verbose_name='Arquivo',
        upload_to='administrativo/oficios_externos/%Y/%m/%d/',
        blank=True,
        validators=[file_validator()]
    )

    class Meta:
        verbose_name = "ADMINISTRATIVO - Ofício Externo"
        verbose_name_plural = "ADMINISTRATIVO - Ofícios Externos"
        permissions = (('view_ato', 'Pode ver esse ato'),)

    def __str__(self):
        return 'Ofício nº {}'.format(self.num_oficio)

    def get_absolute_url(self):
        return reverse('adm:detalhe_processo_adm', kwargs={'pk': self.processo.administrativo.pk})

    def get_tipo_procedimento(self):
        return 'Administrativo - Ofício Recebido'

    def get_procedimento(self):
        return self.processo.administrativo.numero_processo

    def get_origem(self):
        return self.origem

    def get_titulo(self):
        return 'Processo nº {}'.format(self.processo.administrativo.numero_processo)

    def get_criacao(self):
        return timezone.localdate(self.criacao).strftime('%d/%m/%Y')


class DespachoAdm(AtoAdm, Despacho):

    conteudo = models.TextField()

    class Meta:
        verbose_name = "ADMINISTRATIVO - Despacho"
        verbose_name_plural = "ADMINISTRATIVO - Despachos"
        permissions = (('view_ato', 'Pode ver esse ato'),)

    def __str__(self):
        return 'Despacho - {}'.format(self.criacao.strftime('%d/%m/%Y',))


class StatusAdm(AtoAdm):

    LOCAL = (
        (None, 'Escolha o conteúdo principal'),
        ('ASSESSORIA DE IMPRENSA', '1. ASSESSORIA DE IMPRENSA'),
        ('ASSESSORIA DE PLANEJAMENTO', '2. ASSESSORIA DE PLANEJAMENTO'),
        ('ASSESSORIA JURÍDICA', '3. ASSESSORIA JURÍDICA'),
        ('ASSESSORIA MILITAR', '4. ASSESSORIA MILITAR'),
        ('CHEFIA DE GABINETE', '5. CHEFIA DE GABINETE'),
        ('CONSELHO SUPERIOR DE POLÍCIA CIVIL', '6. CONSELHO SUPERIOR DE POLÍCIA CIVIL'),
        (None, '7. DIRETORIA ADMINISTRATIVA FINANCEIRA'),
        ('ASSENTAMENTO FUNCIONAIS', '7.1. ASSENTAMENTO FUNCIONAIS'),
        ('COMISSÃO DE LICITAÇÃO', '7.2. COMISSÃO DE LICITAÇÃO'),
        ('COORDENAÇÃO DE COMPRAS', '7.3. COORDENAÇÃO DE COMPRAS'),
        ('COORDENAÇÃO DE MATERIAL', '7.4. COORDENAÇÃO DE MATERIAL'),
        ('COORDENAÇÃO DE SERVIÇOS GERAIS', '7.5. COORDENAÇÃO DE SERVIÇOS GERAIS'),
        ('COORDENAÇÃO DE SUPRIMENTO DE FUNDOS', '7.6. COORDENAÇÃO DE SUPRIMENTO DE FUNDOS'),
        ('COORDENAÇÃO DE TRANSPORTE', '7.6. COORDENAÇÃO DE TRANSPORTE'),
        ('FOLHA DE PAGAMENTO', '7.7. FOLHA DE PAGAMENTO'),
        ('GERÊNCIA DE ADMINISTRAÇÃO DE RECURSOS DE INFORMÁTICA',
         '7.8. GERÊNCIA DE ADMINISTRAÇÃO DE RECURSOS DE INFORMÁTICA'),
        ('GERÊNCIA DE PESSOAL', '7.9. GERÊNCIA DE PESSOAL'),
        ('GERÊNCIA FINANCEIRA', '7.10. GERÊNCIA FINANCEIRA'),
        ('NÚCLEO DE CONTROLE DE GESTÃO', '7.11. NÚCLEO DE CONTROLE DE GESTÃO'),
        ('PROTOCOLO GERAL', '7.12. PROTOCOLO GERAL'),
        ('SETOR DE ARQUIVO', '7.13. SETOR DE ARQUIVO'),
        ('SETOR DE EMPENHO', '7.14. SETOR DE EMPENHO'),
        ('SETOR DE ENGENHARIA', '7.15. SETOR DE ENGENHARIA'),
        ('SETOR DE INATIVOS', '7.16. SETOR DE INATIVOS'),
        ('DIRETORIA DE GESTÃO INTERNA', '8. DIRETORIA DE GESTÃO INTERNA'),
        ('Outro(s)', 'Outro(s)'),
    )
    local = models.CharField('Localização', max_length=80, choices=LOCAL, blank=True, null=True)
    localizacao = models.ForeignKey(
        LocalizacaoStatusAdm,
        on_delete=models.CASCADE,
        related_name='status',
        verbose_name='Localizacao',
        null=True
    )
    outros = models.CharField('Outro(s)', max_length=100, blank=True)
    situacao = models.CharField('Situação atual', max_length=50)

    class Meta:
        verbose_name = "Administrativo - Status"
        ordering = ['id']

    def __str__(self):
        return 'Status - Processo {} / {} - {}'.format(self.processo.numero_processo, self.local, self.situacao)

    def get_titulo(self):
        return self.situacao


class MidiaAdm(AtoAdm, Midia):

    docs = models.FileField(
        verbose_name='Ofício de origem',
        upload_to='administrativo/midia/%Y/%m/%d/',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "ADMINISTRATIVO - Gravação de mídia"
        verbose_name_plural = "ADMINISTRATIVO - Gravações de mídia"
        permissions = (('view_ato', 'Pode ver esse ato'),)

    def __str__(self):
        return 'Mídia nº: {} - {}'.format(self.num_midia, self.tipo_gravacao_link)

    def get_absolute_url(self):
        return reverse('adm:detalhe_processo_adm', kwargs={'pk': self.processo.administrativo.pk})

    def get_tipo_procedimento(self):
        return 'Administrativo - Mídia'

    def get_origem(self):
        return self.processo.administrativo.oficiante

    def get_procedimento(self):
        return self.processo.administrativo.numero_processo

    def get_titulo(self):
        return 'Processo nº {}'.format(self.processo.administrativo.numero_processo)

    def get_criacao(self):
        return timezone.localdate(self.criacao).strftime('%d/%m/%Y')


class DocumentosGeraisAdm(AtoAdm, Documento):

    nome_doc = models.CharField('Nome do documento', max_length=225, null=False, blank=False)
    documento = models.FileField(
        verbose_name='Arquivo',
        upload_to='administrativo/documento_gerais/%Y/%m/%d/',
        blank=False,
        null=False,
        validators=[file_validator()]
    )

    class Meta:
        verbose_name = "ADMINISTRATIVO - Documento geral"
        verbose_name_plural = "ADMINISTRATIVO - Documentos gerais"
        permissions = (('view_ato', 'Pode ver esse ato'),)

    def __str__(self):
        return f'Documentos Gerais: {self.nome_doc}'

    def get_absolute_url(self):
        return reverse('adm:detalhe_processo_adm', kwargs={'pk': self.processo.administrativo.pk})

    def get_tipo_procedimento(self):
        return 'Administrativo - Documentos Gerais'

    def get_procedimento(self):
        return self.processo.administrativo.numero_processo

    def get_origem(self):
        return self.processo.administrativo.oficiante

    def get_titulo(self):
        return 'Processo nº {}'.format(self.processo.administrativo.numero_processo)

    def get_criacao(self):
        return timezone.localdate(self.criacao).strftime('%d/%m/%Y')

    def get_documento(self):
        return '- {}'.format(self.nome_doc.upper())


class ControlEmpresas(AtoAdm):

    assunto = models.CharField('Assunto', max_length=255)

    class Meta:
        verbose_name = "Controle de Ofício"
        verbose_name_plural = "Controles de Ofícios"

    def __str__(self):
        return self.assunto

    def get_oficios(self):
        return self.ofempresas.all()


class OfEmpresas(CamposComuns, OficioEmpresas):

    controlempresas = models.ForeignKey(
        'ControlEmpresas',
        on_delete=models.CASCADE,
        verbose_name='Ofícios para empresas',
        related_name='ofempresas',
    )
    arquivo = models.FileField(
        verbose_name='Arquivo',
        upload_to='processos/oficios_empresas/%Y/%m/%d/',
        blank=True,
        validators=[file_validator()]
    )

    objects = OfEmpresasManager()

    class Meta:
        verbose_name = "ADMINISTRATIVO - Ofício para empresa"
        verbose_name_plural = "ADMINISTRATIVO - Ofícios para empresas"
        permissions = (
            ('view_ato', 'Pode ver esse ato'),
        )

    def __str__(self):
        return f'Ofício nº {self.num_oficio} - {self.get_empresa_display()}'

    def save(self, *args, **kwargs):
        if not self.autor_id:
            self.autor = self.controlempresas.autor
        if not self.num_oficio:
            self.num_oficio = gerar_numero_documento('OFÍCIOS', self.controlempresas.processo.orgao_processo)
        super(OficioEmpresas, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('adm:detalhe_processo_adm', kwargs={'pk': self.controlempresas.processo.pk})

    def get_tipo_procedimento(self):
        return 'Administrativo - Ofício Empresa(s)'

    def get_origem(self):
        return self.controlempresas.processo.administrativo.oficiante

    def get_procedimento(self):
        return self.controlempresas.processo.__str__()

    def get_titulo(self):
        return f'Processo nº {self.controlempresas.processo.numero_processo}'

    def get_criacao(self):
        return timezone.localdate(self.criacao).strftime('%d/%m/%Y')

    def to_dict_json(self):
        return {
            'ato': self.__str__().upper(),
            'numero': self.controlempresas.processo.numero_processo,
            'nome': "------",
            'tipo': self.controlempresas.processo.get_tipo_procedimento(),
            'criacao': timezone.localtime(self.criacao).strftime('%d/%m/%Y'),
            'link': self.get_absolute_url(),
        }

    def count_obj_by_years(self, orgao=None):
        first_year = 2018
        last_year = timezone.now().year
        dataset = {}
        if orgao:
            while first_year <= last_year:
                total_year = self.__class__.objects \
                    .filter(
                        controlempresas__anulado=False,
                        criacao__year=first_year,
                        controlempresas__processo__orgao_processo=orgao
                    ) \
                    .exclude(arquivo__exact='') \
                    .count()
                dataset.update({first_year: total_year})
                first_year += 1
        else:
            while first_year <= last_year:
                total_year = self.__class__.objects \
                    .filter(controlempresas__anulado=False, criacao__year=first_year) \
                    .exclude(arquivo__exact='') \
                    .count()
                dataset.update({first_year: total_year})
                first_year += 1
        return dataset

    def get_total_nonvoid(self, orgao=None):
        if orgao:
            return self.__class__.objects \
                .filter(controlempresas__anulado=False, controlempresas__processo__orgao_processo=orgao) \
                .exclude(arquivo__exact='') \
                .count()
        return self.__class__.objects \
            .filter(controlempresas__anulado=False) \
            .exclude(arquivo__exact='') \
            .count()


# Auditlog
# ------------------------------------------------------------------------------
auditlog.register(Administrativo)
auditlog.register(OficioInternoAdm)
auditlog.register(OficioExternoAdm)
auditlog.register(DespachoAdm)
auditlog.register(StatusAdm)
auditlog.register(MidiaAdm)
