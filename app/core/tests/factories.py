# from django.db.models.signals import post_save
from datetime import date, datetime
from random import choice

from account.tests.factories import OrgaoFactory, UserFactory
from core.models import (
    AssuntoAdministrativo,
    CamposComuns,
    ConteudoOficioExterno,
    ConteudoOficioInterno,
    Despacho,
    LocalizacaoStatusAdm,
    Midia,
    MotivoVinculo,
    OficioEmpresas,
    OficioExterno,
    OfInterno,
    Processo,
    SequenciaDia,
    SequenciaDocumentos,
    TipoGravacao,
    VinculoProcesso
)
from dateutil.tz import tzlocal
from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, LazyAttribute, Sequence, SubFactory, fuzzy
from factory.faker import faker as FakerLib

faker = FakerLib.Faker(['pt_BR'])
User = get_user_model()


class AssuntoAdministrativoFactory(DjangoModelFactory):

    class Meta:
        model = AssuntoAdministrativo

    assunto = Faker('sentence', nb_words=3)


class TipoGravacaoFactory(DjangoModelFactory):

    class Meta:
        model = TipoGravacao

    tipo = Faker('sentence', nb_words=3)


class LocalizacaoStatusAdmFactory(DjangoModelFactory):

    class Meta:
        model = LocalizacaoStatusAdm

    localizacao = Faker('sentence', nb_words=3)


class ConteudoOficioInternoFactory(DjangoModelFactory):

    class Meta:
        model = ConteudoOficioInterno

    conteudo = Faker('sentence', nb_words=3)


class ConteudoOficioExternoFactory(DjangoModelFactory):

    class Meta:
        model = ConteudoOficioExterno

    conteudo = Faker('sentence', nb_words=3)


class SequenciaDiaFactory(DjangoModelFactory):

    class Meta:
        model = SequenciaDia

    criacao = LazyAttribute(lambda x: faker.date_time(tzinfo=None, end_datetime=None))
    alteracao = LazyAttribute(lambda x: faker.date_time(tzinfo=None, end_datetime=None))
    sequencia = faker.random_int(min=0, max=9999, step=1)


class CamposComunsFactory(DjangoModelFactory):

    class Meta:
        model = CamposComuns
        abstract = True

    criacao = fuzzy.FuzzyDateTime(datetime.now(tz=tzlocal()))
    alteracao = fuzzy.FuzzyDateTime(datetime.now(tz=tzlocal()))
    autor = SubFactory(UserFactory)
    modificador = SubFactory(UserFactory)


class ProcessoFactory(CamposComunsFactory):

    class Meta:
        model = Processo

    numero_processo = Sequence(str)
    # slug = LazyAttribute(lambda x: faker.slug())
    arquivar = faker.boolean(chance_of_getting_true=25)
    arquivador = SubFactory(UserFactory, profile=None)
    data_arquivamento = fuzzy.FuzzyDate(date.today())
    orgao_processo = SubFactory(OrgaoFactory)


class SequenciaDocumentosFactory(DjangoModelFactory):

    class Meta:
        model = SequenciaDocumentos

    criacao = LazyAttribute(lambda x: faker.date_time(tzinfo=None, end_datetime=None))
    alteracao = LazyAttribute(lambda x: faker.date_time(tzinfo=None, end_datetime=None))
    sequencia = faker.random_int(min=0, max=9999, step=1)
    tipo = LazyAttribute(lambda x: faker.name()[:50])


class OficioEmpresasFactory(DjangoModelFactory):
    class Meta:
        model = OficioEmpresas

    empresa = LazyAttribute(lambda x: choice(OficioEmpresas.EMPRESA[1:])[0])
    outros = Faker('name')
    num_oficio = Faker('numerify', text='#'*15)
    data_envio = fuzzy.FuzzyDate(date.today())
    confirmacao = Faker('boolean')
    nome_confirm = LazyAttribute(lambda x: faker.name()[:20])
    conteudo = Faker('text')


class MidiaFactory(DjangoModelFactory):

    class Meta:
        model = Midia

    destino = LazyAttribute(lambda x: faker.name()[:50])
    solicitante = LazyAttribute(lambda x: faker.name()[:80])
    oforigem = LazyAttribute(lambda x: faker.name()[:30])
    tipo_gravacao = LazyAttribute(lambda x: choice(Midia.TIPO_GRAVACAO)[0])
    tipo_gravacao_link = SubFactory(TipoGravacaoFactory)
    num_midia = LazyAttribute(lambda x: faker.name()[:15])


class DespachoFactory(DjangoModelFactory):

    class Meta:
        model = Despacho


class OfInternoFactory(DjangoModelFactory):

    class Meta:
        model = OfInterno

    num_oficio = Faker('numerify', text='##########')
    destino = Faker('sentence', nb_words=3)
    conteudo = SubFactory(ConteudoOficioInternoFactory)
    outros = Faker('sentence', nb_words=3)
    data_envio = Faker('date_between', start_date='-5d')
    confirmacao = Faker('boolean')
    nome_confirm = LazyAttribute(lambda x: faker.name()[:20])


class OficioExternoFactory(DjangoModelFactory):

    class Meta:
        model = OficioExterno

    num_oficio = Sequence(str)
    origem = Faker('lexify', text='?????? ???', letters='ABCDEFGHIJKL')
    conteudo = SubFactory(ConteudoOficioExternoFactory)
    outros = Faker('sentence', nb_words=3)
    data_recebimento = Faker('date_between', start_date='-5d')
    nome_recebimento = Faker('lexify', text='?????? ????', letters='ABCDEFGHIJKL')


class MotivoVinculoFactory(DjangoModelFactory):

    class Meta:
        model = MotivoVinculo

    criacao = fuzzy.FuzzyDateTime(datetime.now(tz=tzlocal()))
    alteracao = fuzzy.FuzzyDateTime(datetime.now(tz=tzlocal()))
    motivo = Faker('sentence', nb_words=2)


class VinculoProcessoFactory(CamposComunsFactory):

    class Meta:
        model = VinculoProcesso

    processo_a = SubFactory(ProcessoFactory)
    processo_b = SubFactory(ProcessoFactory)
    motivo_vinculo = SubFactory(MotivoVinculoFactory)
