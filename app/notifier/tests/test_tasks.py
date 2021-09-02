from django.core import serializers
from django.test import TestCase

from ..helper import SingleNotificationDisplay
from ..tasks import notificar, on_email
from .factories import NotificationFactory


class NotificarTestCase(TestCase):

    def setUp(self):
        self.notice = NotificationFactory()

    def test_notificar(self):
        actor = self.notice.actor
        users = self.notice.recipient
        verb = self.notice.verb
        target = self.notice.target
        obj = self.notice.action_object

        notification_context = {
            'actor': serializers.serialize('json', [actor]),
            'users': serializers.serialize('json', [users]),
            'verb': verb,
            'target': serializers.serialize('json', [target]),
            'action_object': serializers.serialize('json', [obj]),
            'description': target.get_absolute_url()
        }
        notificar(notification_context, True)


class OnEmailTestCase(TestCase):

    def setUp(self):
        self.notice = NotificationFactory.build()
        self.hp = SingleNotificationDisplay(self.notice)

    def test_send_email(self):
        user_emails = self.notice.recipient.email

        email_context = {
            'msg': self.hp.get_notify_msg(),
            'user_emails': [user_emails],
            'unsent_notices': serializers.serialize('json', [self.notice])
        }

        on_email(email_context, True)
