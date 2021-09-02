import factory
from account.tests.factories import UserFactory
from adm.models import (
    Administrativo,
    AtoAdm,
    DespachoAdm,
    DocumentosGeraisAdm,
    MidiaAdm,
    OficioExternoAdm,
    OficioInternoAdm,
    StatusAdm
)
from core.tests.factories import (
    AssuntoAdministrativoFactory,
    CamposComunsFactory,
    LocalizacaoStatusAdmFactory,
    OficioExternoFactory,
    OfInternoFactory,
    ProcessoFactory,
    TipoGravacaoFactory
)


class AdministrativoFactory(ProcessoFactory):

    class Meta:
        model = Administrativo

    assunto_adm = factory.SubFactory(AssuntoAdministrativoFactory)
    outro = factory.Faker('sentence', nb_words=3)
    destino_adm = factory.Faker('sentence', nb_words=3)
    oficiante = factory.Faker('lexify', text='?????', letters='DINT')
    email = factory.Faker('email')
    fone = factory.Faker('lexify', text='(8?)9????-????', letters='1234567890')
    observacao = factory.Faker('paragraph', nb_sentences=1)
    arquivo = factory.django.FileField(data=b'E'*300, filename="arquivo_de_testes.pdf")
    arquivar = False


class AtoAdmFactory(CamposComunsFactory):

    class Meta:
        model = AtoAdm
        abstract = True

    processo = factory.SubFactory(AdministrativoFactory)
    autor = factory.SubFactory(UserFactory)
    criacao = factory.Faker('date_between', start_date='-0d')


class OficioInternoAdmFactory(AtoAdmFactory, OfInternoFactory):

    class Meta:
        model = OficioInternoAdm

    tipo_ato = '1'
    arquivo = factory.django.FileField(data=b'E'*300, filename="arquivo_de_testes.pdf")


class OficioExternoAdmFactory(AtoAdmFactory, OficioExternoFactory):

    class Meta:
        model = OficioExternoAdm

    tipo_ato = '2'
    arquivo = factory.django.FileField(data=b'E'*300, filename="arquivo_de_testes.pdf")


class DespachoAdmFactory(AtoAdmFactory):

    class Meta:
        model = DespachoAdm

    tipo_ato = '3'
    conteudo = factory.Faker('paragraph', nb_sentences=3)


class StatusAdmFactory(AtoAdmFactory):

    class Meta:
        model = StatusAdm

    tipo_ato = '4'
    localizacao = factory.SubFactory(LocalizacaoStatusAdmFactory)
    situacao = factory.Faker('sentence', nb_words=3)
    descricao = factory.Faker('sentence', nb_words=3)


class MidiaAdmFactory(AtoAdmFactory):

    class Meta:
        model = MidiaAdm

    tipo_ato = '5'
    destino = factory.Faker('sentence', nb_words=3)
    solicitante = factory.Faker('sentence', nb_words=3)
    oforigem = factory.Faker('sentence', nb_words=1)
    tipo_gravacao_link = factory.SubFactory(TipoGravacaoFactory)
    docs = factory.django.FileField(data=b'E'*300, filename="arquivo_de_testes.pdf")


class DocumentoAdmFactory(AtoAdmFactory):

    class Meta:
        model = DocumentosGeraisAdm

    tipo_ato = '6'
    documento = factory.django.FileField(data=b'E'*300, filename="arquivo_de_testes.pdf")
    motivo_anulacao = factory.Faker('sentence', nb_words=3)
    nome_doc = factory.Faker('word')
