from django.core import mail
from django.test import TestCase

from ..utils import send_to_email_users
from .factories import NotificationFactory


class EmailTest(TestCase):
    def test_send_email(self):
        # Send message.
        mail.send_mail(
            'Subject here', 'Here is the message.',
            'from@example.com', ['to@example.com'],
            fail_silently=False,
        )

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Subject here')

    def test_send_to_email_users(self):

        email_context = {
            'msg': 'Here is the message.',
            'user_emails': ['to@example.com'],
            'unsent_notices': [NotificationFactory()]
        }
        send_to_email_users(email_context, test=True)
