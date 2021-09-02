from blog.tests.factories import PostFactory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..helper import NotificationDirectorDisplay, NotificationUserDisplay, SingleNotificationDisplay
from .factories import NotificationFactory, TelegramUserFactory


class SingleNotificationDisplayTestCase(TestCase):

    def setUp(self):
        self.nt = NotificationFactory()
        self.sn = SingleNotificationDisplay(self.nt)
        self.tu = TelegramUserFactory(user=self.nt.recipient, allowed=True)

    def test_notification_dict(self):
        dic = {
            "msg": self.sn.get_notify_msg(),
            "recipient_tgram": self.sn.get_telegram()
        }
        self.assertEqual(dic, self.sn.notification_dict())

    def test_get_notify_msg(self):
        if self.nt.verb != 'solicitar':
            self.assertTrue(self.nt.actor.get_full_name().lower() in self.sn.get_notify_msg().lower())
            self.assertTrue(self.nt.verb.lower() in self.sn.get_notify_msg().lower())
        else:
            self.assertTrue(self.nt.description.title().lower() in self.sn.get_notify_msg().lower())

    def test_get_actor(self):
        self.assertEqual(self.nt.actor.get_full_name().title(), self.sn.get_actor(self.nt))

    def test_message_verb_incluiu(self):
        actor = self.sn.get_actor(self.nt)
        processo = self.nt.target.get_notification_label()

        msg = f'{actor} {self.nt.verb} você no {processo}'
        self.assertEqual(self.sn.message_verb_incluiu(self.nt), msg)

    def test_message_verb_notificou(self):
        actor = self.sn.get_actor(self.nt)
        ato = self.nt.action_object
        processo = self.nt.target.get_notification_label()

        msg = f'{actor} {self.nt.verb} você sobre {ato} no {processo}'
        self.assertEqual(self.sn.message_verb_notificou(self.nt), msg)

    def test_message_verb_publicou(self):
        self.nt.target = PostFactory()
        actor = self.sn.get_actor(self.nt)
        post = self.nt.target.truncate_titulo(50)

        msg = f'{actor} {self.nt.verb} o post: {post}'
        self.assertEqual(self.sn.message_verb_publicou(self.nt), msg)

    def test_message_verb_removeu(self):
        actor = self.sn.get_actor(self.nt)
        processo = self.nt.target.get_notification_label()

        msg = f'{actor} {self.nt.verb} você do {processo}'
        self.assertEqual(self.sn.message_verb_removeu(self.nt), msg)

    def test_message_verb_solicitar(self):
        msg = f'Bot Telegram: permita que as notificações sejam enviadas para {self.nt.description.title()}.'
        self.assertEqual(self.sn.message_verb_solicitar(self.nt), msg)


class NotificationDirectorDisplayTestCase(TestCase):

    def setUp(self):
        self.nt = NotificationFactory.create_batch(10)
        self.sn = NotificationDirectorDisplay(self.nt)

    def test_notification_dict(self):
        dic = {
            "data": timezone.localtime(self.nt[0].timestamp).strftime('%d/%m/%Y'),
            "msg": self.sn.get_notify_msg(self.nt[0]),
            "receptor": self.nt[0].recipient.__str__(),
            "lida": self.nt[0].unread,
            "procedimento": self.nt[0].target.get_tipo_procedimento(),
            "link": self.nt[0].target.get_absolute_url()
        }
        self.assertEqual(dic, self.sn.notification_dict(self.nt[0]))

    def test_get_notifications_context(self):
        dics = [{
            "data": timezone.localtime(notice.timestamp).strftime('%d/%m/%Y'),
            "msg": self.sn.get_notify_msg(notice),
            "receptor": notice.recipient.__str__(),
            "lida": notice.unread,
            "procedimento": notice.target.get_tipo_procedimento(),
            "link": notice.target.get_absolute_url()
        } for notice in self.nt]

        self.assertEqual(dics, self.sn.get_notifications_context())

    def test_get_notify_msg(self):
        if self.nt[1].verb != 'solicitar':
            self.assertTrue(self.nt[1].actor.get_full_name().lower() in self.sn.get_notify_msg(self.nt[1]).lower())
            self.assertTrue(self.nt[1].verb.lower() in self.sn.get_notify_msg(self.nt[1]).lower())
        else:
            self.assertTrue(self.nt[1].description.lower() in self.sn.get_notify_msg(self.nt[1]).lower())

    def test_get_actor(self):
        self.assertEqual(self.nt[2].actor.get_full_name().title(), self.sn.get_actor(self.nt[2]))

    def test_message_verb_incluiu(self):
        actor = self.sn.get_actor(self.nt[3])
        processo = self.nt[3].target.get_notification_label()
        notificado = self.nt[3].recipient.get_full_name().title()

        msg = f'{actor} {self.nt[3].verb} {notificado} no {processo}'
        self.assertEqual(self.sn.message_verb_incluiu(self.nt[3]), msg)

    def test_message_verb_notificou(self):
        actor = self.sn.get_actor(self.nt[4])
        ato = self.nt[4].action_object
        processo = self.nt[4].target.get_notification_label()
        notificado = self.nt[4].recipient.get_full_name().title()

        msg = f'{actor} {self.nt[4].verb} {notificado} sobre {ato} no {processo}'
        self.assertEqual(self.sn.message_verb_notificou(self.nt[4]), msg)

    def test_message_verb_publicou(self):
        self.nt[5].target = PostFactory()
        actor = self.sn.get_actor(self.nt[5])
        post = self.nt[5].target.truncate_titulo(50)

        msg = f'{actor} {self.nt[5].verb} o post: {post}'
        self.assertEqual(self.sn.message_verb_publicou(self.nt[5]), msg)

    def test_message_verb_removeu(self):
        actor = self.sn.get_actor(self.nt[6])
        processo = self.nt[6].target.get_notification_label()
        notificado = self.nt[6].recipient.get_full_name().title()

        msg = f'{actor} {self.nt[6].verb} {notificado} do {processo}'
        self.assertEqual(self.sn.message_verb_removeu(self.nt[6]), msg)

    def test_message_verb_solicitar(self):
        tgram_user = self.nt[7].description.title()
        gep_user = self.nt[7].actor.get_full_name().title()
        msg = f'{tgram_user} solicitou ser notificado como {gep_user}'
        self.assertEqual(self.sn.message_verb_solicitar(self.nt[7]), msg)


class NotificationUserDisplayTestCase(TestCase):

    def setUp(self):
        self.nt = NotificationFactory.create_batch(10)
        self.sn = NotificationUserDisplay(self.nt)

    def test_notification_dict(self):
        dic = {
            "data": timezone.localtime(self.nt[0].timestamp).strftime('%d/%m/%Y'),
            "msg": self.sn.get_notify_msg(self.nt[0]),
            "procedimento": self.nt[0].target.get_tipo_procedimento(),
            "link": self.nt[0].target.get_absolute_url(),
            "lida": self.nt[0].unread,
            "id": self.nt[0].id,
            "url": reverse('account:notificacao_lida')
        }
        self.assertEqual(dic, self.sn.notification_dict(self.nt[0]))

    def test_get_notify_msg(self):
        if (self.nt[1].verb != 'solicitar'):
            self.assertTrue(self.nt[1].actor.get_full_name().lower() in self.sn.get_notify_msg(self.nt[1]).lower())
            self.assertTrue(self.nt[1].verb.lower() in self.sn.get_notify_msg(self.nt[1]).lower())
        else:
            self.assertTrue(self.nt[1].description.lower() in self.sn.get_notify_msg(self.nt[1]).lower())

    def test_get_actor(self):
        self.assertEqual(self.nt[2].actor.get_full_name().title(), self.sn.get_actor(self.nt[2]))

    def test_message_verb_incluiu(self):
        actor = self.sn.get_actor(self.nt[3])
        processo = self.nt[3].target.get_notification_label()

        msg = f'{actor} {self.nt[3].verb} você no {processo}'
        self.assertEqual(self.sn.message_verb_incluiu(self.nt[3]), msg)

    def test_message_verb_notificou(self):
        actor = self.sn.get_actor(self.nt[4])
        ato = self.nt[4].action_object
        processo = self.nt[4].target.get_notification_label()

        msg = f'{actor} {self.nt[4].verb} você sobre {ato} no {processo}'
        self.assertEqual(self.sn.message_verb_notificou(self.nt[4]), msg)

    def test_message_verb_publicou(self):
        self.nt[6].target = PostFactory()
        actor = self.sn.get_actor(self.nt[6])
        post = self.nt[6].target.truncate_titulo(50)

        msg = f'{actor} {self.nt[6].verb} o post: {post}'
        self.assertEqual(self.sn.message_verb_publicou(self.nt[6]), msg)

    def test_message_verb_removeu(self):
        actor = self.sn.get_actor(self.nt[6])
        processo = self.nt[6].target.get_notification_label()

        msg = f'{actor} {self.nt[6].verb} você do {processo}'
        self.assertEqual(self.sn.message_verb_removeu(self.nt[6]), msg)

    def test_message_verb_solicitar(self):
        msg = f'Bot Telegram: permita que as notificações sejam enviadas para {self.nt[7].description.title()}.'
        self.assertEqual(self.sn.message_verb_solicitar(self.nt[7]), msg)
