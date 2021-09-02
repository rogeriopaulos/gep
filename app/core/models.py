# -*- coding: utf-8 -*-

from datetime import date

from account.models import Orgao
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


# Tabelas de Normalização
# ------------------------------------------------------------------------------
class AssuntoAdministrativo(models.Model):

    assunto = models.CharField('Assunto', max_length=255)

    class Meta:
        verbose_name = '[NORMALIZAÇÃO] Assunto (Administrativo)'
        verbose_name_plural = '[NORMALIZAÇÃO] Assuntos (Administrativo)'
        ordering = ['assunto']

    def __str__(self):
        return self.assunto


class TipoGravacao(models.Model):

    tipo = models.CharField('Tipo', max_length=255)

    class Meta:
        verbose_name = '[NORMALIZAÇÃO] Tipo de gravação de mídia'
        verbose_name_plural = '[NORMALIZAÇÃO] Tipos de gravações de mídia'
        ordering = ['tipo']

    def __str__(self):
        return self.tipo


class LocalizacaoStatusAdm(models.Model):

    localizacao = models.CharField('Localização', max_length=255)

    class Meta:
        verbose_name = '[NORMALIZAÇÃO] Status (Administrativo)'
        verbose_name_plural = '[NORMALIZAÇÃO] Status (Administrativo)'
        ordering = ['localizacao']

    def __str__(self):
        return self.localizacao


class ConteudoOficioInterno(models.Model):

    conteudo = models.CharField('Conteúdo', max_length=255)

    class Meta:
        verbose_name = '[NORMALIZAÇÃO] Conteúdo - Of. Expedido'
        verbose_name_plural = '[NORMALIZAÇÃO] Conteúdos - Of. Expedidos'
        ordering = ['conteudo']

    def __str__(self):
        return self.conteudo


class ConteudoOficioExterno(models.Model):

    conteudo = models.CharField('Conteúdo', max_length=255)

    class Meta:
        verbose_name = '[NORMALIZAÇÃO] Conteúdo - Of. Recebido'
        verbose_name_plural = '[NORMALIZAÇÃO] Conteúdos - Of. Recebidos'
        ordering = ['conteudo']

    def __str__(self):
        return self.conteudo


# ------------------------------------------------------------------------------
class SequenciaDia(models.Model):
    """
    Parte da lógica que gera número dos processos
    """
    criacao = models.DateTimeField('Criado em', auto_now_add=True, null=True)
    alteracao = models.DateTimeField('Alterado em ', auto_now=True, null=True)
    sequencia = models.PositiveIntegerField('Num de Sequência', unique_for_date='criacao')

    class Meta:
        verbose_name = 'Número de sequência de Processos'
        verbose_name_plural = 'Números de sequência de Processos'

    def __str__(self):
        return 'Sequência: {}'.format(self.sequencia)


class CamposComuns(models.Model):
    """
    Campos que serão comuns na maioria das tabelas.
    """
    criacao = models.DateTimeField('Criado em', auto_now_add=True, null=True)
    alteracao = models.DateTimeField('Alterado em ', auto_now=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_autor')
    modificador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_modificador',
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
        ordering = ['criacao']


class Processo(CamposComuns):
    """
    Tabela que indexa os números de processo.
    Processo geral; engloba todos os atos.
    """
    numero_processo = models.CharField('Número do processo', max_length=13, unique=True)
    slug = models.SlugField(max_length=255, blank=True)
    orgao_processo = models.ForeignKey(
        Orgao,
        on_delete=models.CASCADE,
        related_name='processos',
        verbose_name='Instituição a qual está vinculado',
        null=True
    )
    arquivar = models.BooleanField('Arquivar processo', default=False)
    arquivador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='%(class)s_arquivador'
    )
    data_arquivamento = models.DateField('Arquivado em', null=True, blank=True)

    class Meta:
        verbose_name = "Processo"
        verbose_name_plural = "Processos"
        ordering = ['numero_processo']

    def __str__(self):
        return self.numero_processo

    def gerar_numero_processo(self):
        """
        Gera o número do processo baseado no padrão: 0000[sequencia]-MM/AAAA
        """
        ano_atual = date.today().year
        ultimo = SequenciaDia.objects.last()
        if ultimo and ultimo.criacao.date().year == ano_atual:
            novonum_seq = SequenciaDia()
            novonum_seq.sequencia = ultimo.sequencia + 1
            novonum_seq.save()
        else:
            novonum_seq = SequenciaDia()
            novonum_seq.sequencia = 1
            novonum_seq.save()
        str_novonum = str(novonum_seq.sequencia)
        tamanho = len(str_novonum)
        zeros = ['0' for i in range(5 - tamanho)]
        zeros.append(str_novonum)
        zeros.append('-')
        num1 = ''.join(zeros)
        hoje = date.today()
        num2 = hoje.strftime("%m/%Y")
        self.numero_processo = num1 + num2

    def get_nome_op(self):
        return None

    def to_dict_json(self):
        return {
            'numero': self.numero_processo,
            'nome': self.get_nome_op(),
            'tipo': self.get_tipo_procedimento(),
            'criacao': timezone.localtime(self.criacao).strftime('%d/%m/%Y'),
            'link': self.get_absolute_url(),
        }

    def get_kwarg_url(self):
        return self.slug if self.slug else self.pk


def gerar_numero_documento(tipo, orgao):
    hoje = date.today()
    sequencias = SequenciaDocumentos.objects.filter(tipo=tipo)
    ultimo = sequencias.filter(orgao=orgao).last()
    if ultimo and ultimo.criacao.year == hoje.year:
        novonum_seq = ultimo
        novonum_seq.sequencia += 1
        novonum_seq.save()
    else:
        novonum_seq = SequenciaDocumentos()
        novonum_seq.sequencia = 1
        novonum_seq.tipo = tipo
        novonum_seq.orgao = orgao
        novonum_seq.save()
    str_novonum = str(novonum_seq.sequencia)
    tamanho = len(str_novonum)
    zeros = ['0' for i in range(5 - tamanho)]
    zeros.append(str_novonum)
    num1 = ''.join(zeros)
    num2 = hoje.strftime("%Y")

    if orgao:
        sigla = '/{}/'.format(orgao.sigla)
        numero_processo = num1 + sigla + num2
        return numero_processo

    numero_processo = num1 + '/' + num2
    return numero_processo


class SequenciaDocumentos(models.Model):
    criacao = models.DateTimeField('Criado em', auto_now_add=True, null=True)
    alteracao = models.DateTimeField('Alterado em', auto_now=True, null=True)
    sequencia = models.PositiveIntegerField(verbose_name='Nº Sequencial')
    tipo = models.CharField('Tipo de documento', max_length=50)
    orgao = models.ForeignKey(
        Orgao,
        on_delete=models.CASCADE,
        related_name='sequencias',
        verbose_name='Órgão referencial',
        null=True
    )

    class Meta:
        verbose_name = 'Número de sequência de documentos'
        verbose_name_plural = 'Números de sequência de documentos'

    def __str__(self):
        if self.orgao:
            return f'{self.tipo} nº {self.sequencia} ({self.orgao.sigla})'
        else:
            return f'{self.tipo} nº {self.sequencia}'


class OficioEmpresas(models.Model):

    EMPRESA = (
        (None, 'Selecione uma empresa'),
        ('1', 'Vivo'),
        ('2', 'Claro'),
        ('3', 'TIM'),
        ('4', 'Oi'),
        ('5', 'Algar'),
        ('6', 'Sercomtel'),
        ('7', 'Aeiou (Unicel)'),
        ('8', 'Nextel'),
        ('9', 'Transit'),
        ('10', 'Sky'),
        ('11', 'Telebras'),
        ('12', 'GVT'),
        ('13', 'Google'),
        ('14', 'Apple'),
        ('15', 'Microsoft'),
        ('16', 'NET'),
        ('17', 'Facebook'),
        ('18', 'Instagram'),
        ('19', 'Twitter'),
        ('20', 'Whatsapp'),
        ('21', 'Outros'),
    )
    empresa = models.CharField('Destinatário', max_length=2, choices=EMPRESA)
    outros = models.CharField('Nome (Empresa)', max_length=80, blank=True)
    num_oficio = models.CharField('Número do Ofício', max_length=255)
    autoridade = models.CharField('Autoridade Policial que Subscreve', max_length=80)
    data_envio = models.DateField('Data de envio do ofício', null=True, blank=True)
    confirmacao = models.BooleanField('Ofício recebido', default=False, blank=True)
    nome_confirm = models.CharField('Funcionário | Protocolo', blank=True, max_length=20)
    conteudo = models.TextField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.num_oficio:
            self.num_oficio = gerar_numero_documento('OFÍCIOS', self.processo.orgao_processo)
        super(OficioEmpresas, self).save(*args, **kwargs)


class Midia(models.Model):

    destino = models.CharField('Destinatário', max_length=50)
    solicitante = models.CharField('Órgão/Autoridade solicitante', max_length=80)
    oforigem = models.CharField('Ofício de origem', max_length=30, blank=True)
    TIPO_GRAVACAO = (
        ('1', 'Integralidade dos áudios'),
        ('2', 'Áudios relevantes'),
        ('3', 'Áudios selecionados'),
        ('4', 'Gravação de Dados')
    )
    tipo_gravacao = models.CharField('Tipo de gravação', max_length=1, choices=TIPO_GRAVACAO, blank=True, null=True)
    tipo_gravacao_link = models.ForeignKey(
        TipoGravacao,
        on_delete=models.CASCADE,
        verbose_name='Tipo de gravação',
        null=True
    )
    num_midia = models.CharField('Gerar Número', max_length=255)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.num_midia:
            self.num_midia = gerar_numero_documento('GRAVAÇÃO DE MÍDIA', self.processo.orgao_processo)
        super(Midia, self).save(*args, **kwargs)

    def count_obj_by_years(self, orgao=None):
        first_year = 2018
        last_year = timezone.now().year
        dataset = {}
        if orgao:
            while first_year <= last_year:
                total_year = self.__class__.objects.filter(
                    anulado=False, criacao__year=first_year, processo__orgao_processo=orgao).count()
                dataset.update({first_year: total_year})
                first_year += 1

        else:
            while first_year <= last_year:
                total_year = self.__class__.objects.filter(anulado=False, criacao__year=first_year).count()
                dataset.update({first_year: total_year})
                first_year += 1
        return dataset

    def get_total_nonvoid(self, orgao=None):
        if orgao:
            return self.__class__.objects.filter(anulado=False, processo__orgao_processo=orgao).count()
        return self.__class__.objects.filter(anulado=False).count()


class Despacho(models.Model):

    class Meta:
        abstract = True

    def count_obj_by_years(self, orgao=None):
        first_year = 2018
        last_year = timezone.now().year
        dataset = {}
        if orgao:
            while first_year <= last_year:
                total_year = self.__class__.objects.filter(
                    anulado=False, criacao__year=first_year, processo__orgao_processo=orgao).count()
                dataset.update({first_year: total_year})
                first_year += 1

        else:
            while first_year <= last_year:
                total_year = self.__class__.objects.filter(anulado=False, criacao__year=first_year).count()
                dataset.update({first_year: total_year})
                first_year += 1
        return dataset

    def get_total_nonvoid(self, orgao=None):
        if orgao:
            return self.__class__.objects.filter(anulado=False, processo__orgao_processo=orgao).count()
        return self.__class__.objects.filter(anulado=False).count()


class OfInterno(models.Model):

    num_oficio = models.CharField('Gerar Número', max_length=255)
    destino = models.CharField('Destinatário', max_length=140)
    conteudo = models.ForeignKey(
        ConteudoOficioInterno,
        on_delete=models.CASCADE,
        verbose_name='Conteúdo principal',
        null=True
    )
    outros = models.CharField('Outro(s)', max_length=140, blank=True)
    autoridade = models.CharField('Autoridade Policial que subscreve', max_length=80)
    data_envio = models.DateField('Recebido em', null=True, blank=True)
    confirmacao = models.BooleanField('Ofício recebido', default=False, blank=True)
    nome_confirm = models.CharField('Funcionário/Pessoa que confirmou', max_length=20, blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.num_oficio:
            self.num_oficio = gerar_numero_documento('OFÍCIOS', self.processo.orgao_processo)
        super(OfInterno, self).save(*args, **kwargs)

    def count_obj_by_years(self, orgao=None):
        first_year = 2018
        last_year = timezone.now().year
        dataset = {}
        if orgao:
            while first_year <= last_year:
                total_year = self.__class__.objects.filter(
                    anulado=False,
                    criacao__year=first_year,
                    processo__orgao_processo=orgao).exclude(arquivo__exact='').count()
                dataset.update({first_year: total_year})
                first_year += 1

        else:
            while first_year <= last_year:
                total_year = self.__class__.objects.filter(
                    anulado=False, criacao__year=first_year).exclude(arquivo__exact='').count()
                dataset.update({first_year: total_year})
                first_year += 1
        return dataset

    def get_total_nonvoid(self, orgao=None):
        if orgao:
            return self.__class__.objects.filter(
                anulado=False, processo__orgao_processo=orgao).exclude(arquivo__exact='').count()
        return self.__class__.objects.filter(anulado=False).exclude(arquivo__exact='').count()


class OficioExterno(models.Model):

    num_oficio = models.CharField('Número do ofício', max_length=140)
    origem = models.CharField('Autoridade/Órgão de origem', max_length=50)
    conteudo = models.ForeignKey(
        ConteudoOficioExterno,
        on_delete=models.CASCADE,
        verbose_name='Conteúdo principal',
        null=True
    )
    outros = models.CharField('Outros', max_length=140, blank=True)
    data_recebimento = models.DateField('Data de recebimento')
    nome_recebimento = models.CharField('Funcionário que recebeu', max_length=40)

    class Meta:
        abstract = True

    def count_obj_by_years(self, orgao=None):
        first_year = 2018
        last_year = timezone.now().year
        dataset = {}
        if orgao:
            while first_year <= last_year:
                total_year = self.__class__.objects.filter(
                    anulado=False,
                    criacao__year=first_year,
                    processo__orgao_processo=orgao).exclude(arquivo__exact='').count()
                dataset.update({first_year: total_year})
                first_year += 1

        else:
            while first_year <= last_year:
                total_year = self.__class__.objects.filter(
                    anulado=False, criacao__year=first_year).exclude(arquivo__exact='').count()
                dataset.update({first_year: total_year})
                first_year += 1
        return dataset

    def get_total_nonvoid(self, orgao=None):
        if orgao:
            return self.__class__.objects.filter(
                anulado=False, processo__orgao_processo=orgao).exclude(arquivo__exact='').count()
        return self.__class__.objects.filter(anulado=False).exclude(arquivo__exact='').count()


class MotivoVinculo(models.Model):

    criacao = models.DateTimeField('Criado em', auto_now_add=True, null=True)
    alteracao = models.DateTimeField('Alterado em ', auto_now=True, null=True)
    motivo = models.CharField('Motivo', max_length=255)

    class Meta:
        verbose_name = "[NORMALIZAÇÃO] Processo vinculado - Motivo"
        verbose_name_plural = "[NORMALIZAÇÃO] Processos vinculados - Motivos"

    def __str__(self):
        return f'{self.motivo}'


class VinculoProcesso(CamposComuns):

    processo_a = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='processoa_vinculos')
    processo_b = models.ForeignKey(
        Processo,
        on_delete=models.CASCADE,
        related_name='processob_vinculos',
        verbose_name='Informe o número do processo vinculado'
    )
    motivo_vinculo = models.ForeignKey(
        MotivoVinculo,
        on_delete=models.CASCADE,
        verbose_name='Informe o motivo da vinculação',
        related_name='vinculos',
        null=True
    )

    class Meta:
        verbose_name = "Processo vinculado"
        verbose_name_plural = "Processos vinculados"
        ordering = ['criacao']
        unique_together = (("processo_a", "processo_b"),)

    def __str__(self):
        return f'{self.processo_a} - {self.processo_b}'


class Documento(models.Model):

    class Meta:
        abstract = True

    def count_obj_by_years(self, orgao=None):
        first_year = 2018
        last_year = timezone.now().year
        dataset = {}
        if orgao:
            while first_year <= last_year:
                total_year = self.__class__.objects.filter(
                    anulado=False, criacao__year=first_year, processo__orgao_processo=orgao).count()
                dataset.update({first_year: total_year})
                first_year += 1

        else:
            while first_year <= last_year:
                total_year = self.__class__.objects.filter(anulado=False, criacao__year=first_year).count()
                dataset.update({first_year: total_year})
                first_year += 1
        return dataset

    def get_total_nonvoid(self, orgao=None):
        if orgao:
            return self.__class__.objects.filter(anulado=False, processo__orgao_processo=orgao).count()
        return self.__class__.objects.filter(anulado=False).count()
