from random import choice

from account.models import Cargo, Orgao, Profile
from account.utils import CARGOS, INSTITUICOES
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from factory import DjangoModelFactory, Faker, Sequence, SubFactory, django

User = get_user_model()


@django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    id = Sequence(lambda x: 12345+x)
    username = Sequence(lambda x: f'agent{x}')
    first_name = Faker('first_name', locale='pt_BR')
    last_name = Faker('last_name', locale='pt_BR')

    email = Faker('ascii_free_email', locale='pt_BR')
    password = Faker('password', locale='pt_BR', length=12, digits=True, upper_case=True, lower_case=True)


class OrgaoFactory(DjangoModelFactory):

    class Meta:
        model = Orgao

    orgao = choice(INSTITUICOES)[1]
    sigla = Faker('word')


class CargoFactory(DjangoModelFactory):

    class Meta:
        model = Cargo

    orgao = SubFactory(OrgaoFactory)
    cargo = choice(CARGOS)[1]


@django.mute_signals(post_save)
class ProfileFactory(DjangoModelFactory):

    class Meta:
        model = Profile

    user = SubFactory('account.tests.factories.UserFactory')
    nascimento = Faker('date_of_birth', minimum_age=18, maximum_age=80)

    orgao_link = SubFactory('account.tests.factories.OrgaoFactory')

    cargo_link = SubFactory('account.tests.factories.CargoFactory')

    lotacao = Faker('word')
    funcao = Faker('word')
    matricula = Faker('random_number', locale='pt_BR', digits=9)
    cpf = Faker('cpf', locale='pt_BR')
    identidade = Faker('rg', locale='pt_BR')
    org_identidade = Faker('lexify', text='???', letters='spiaue')
    cel_funcional = Faker('lexify', text='(8?)9????-????', letters='1234567890')
    cel_pessoal = Faker('lexify', text='(8?)9????-????', letters='1234567890')
    endereco = Faker('street_address', locale='pt_BR')
    cep = Faker('postcode', locale='pt_BR')
