from random import choice

from account.tests.factories import UserFactory
from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Faker, LazyAttribute, SubFactory
from notifications.models import Notification
from quebra.tests.factories import QuebraFactory

from ..models import TelegramUser
from . import utils

User = get_user_model()

verbs = [
    'incluiu',
    'notificou',
    # 'publicou',
    'removeu',
    'solicitar'
]


class NotificationFactory(DjangoModelFactory):

    class Meta:
        model = Notification

    actor = SubFactory(UserFactory)
    recipient = SubFactory(UserFactory)
    verb = LazyAttribute(lambda x: choice(verbs))
    action_object = SubFactory(choice(
        utils.factories['adm'] +
        utils.factories['lab'] +
        utils.factories['intel'] +
        utils.factories['inter'] +
        utils.factories['quebra']
    ))
    target = SubFactory(choice(
        [
            # AdministrativoFactory,
            # InteligenciaFactory,
            # InterceptacaoFactory,
            # LabFactory,
            QuebraFactory
        ]
    ))
    description = Faker('paragraph')


class TelegramUserFactory(DjangoModelFactory):

    class Meta:
        model = TelegramUser

    user = SubFactory(UserFactory)
    chat_id = Faker('numerify', text='######')
    allowed = Faker('boolean')
    chat_fullname = Faker('name')
