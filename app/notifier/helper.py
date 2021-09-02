# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _


class NotificationManagerDisplay(metaclass=ABCMeta):

    def __init__(self, notifications):
        self.notifications = notifications

    def get_notifications_context(self):
        return [self.notification_dict(nt) for nt in self.notifications]

    @abstractmethod
    def notification_dict(self, notification):
        ...  # pragma: no cover

    def get_notify_msg(self, nt):
        msgs = {
            'incluiu': self.message_verb_incluiu,
            'notificou': self.message_verb_notificou,
            'publicou': self.message_verb_publicou,
            'removeu': self.message_verb_removeu,
            'solicitar': self.message_verb_solicitar,
        }

        return msgs[nt.verb](nt) if nt.verb in msgs.keys() else _(str(nt))

    @abstractmethod
    def get_actor(self, notification):
        ...  # pragma: no cover

    @abstractmethod
    def message_verb_incluiu(self, notification):
        ...  # pragma: no cover

    @abstractmethod
    def message_verb_notificou(self, notification):
        ...  # pragma: no cover

    @abstractmethod
    def message_verb_publicou(self, notification):
        ...  # pragma: no cover

    @abstractmethod
    def message_verb_removeu(self, notification):
        ...  # pragma: no cover

    @abstractmethod
    def message_verb_solicitar(self, notification):
        ...  # pragma: no cover


class NotificationUserDisplay(NotificationManagerDisplay):

    def notification_dict(self, notification):
        return {
            "data": timezone.localtime(notification.timestamp).strftime('%d/%m/%Y'),
            "msg": self.get_notify_msg(notification),
            "procedimento": notification.target.get_tipo_procedimento(),
            "link": notification.target.get_absolute_url(),
            "lida": notification.unread,
            "id": notification.id,
            "url": reverse('account:notificacao_lida')
        }

    def get_actor(self, notification):
        return notification.actor.get_full_name().title()

    def message_verb_incluiu(self, notification):
        actor = self.get_actor(notification)
        processo = notification.target.get_notification_label()

        return f'{actor} {notification.verb} você no {processo}'

    def message_verb_notificou(self, notification):
        actor = self.get_actor(notification)
        ato = notification.action_object
        processo = notification.target.get_notification_label()

        return f'{actor} {notification.verb} você sobre {ato} no {processo}'

    def message_verb_publicou(self, notification):
        actor = self.get_actor(notification)
        post = notification.target.truncate_titulo(50)

        return f'{actor} {notification.verb} o post: {post}'

    def message_verb_removeu(self, notification):
        actor = self.get_actor(notification)
        processo = notification.target.get_notification_label()

        return f'{actor} {notification.verb} você do {processo}'

    def message_verb_solicitar(self, notification):
        tgram_user = notification.description

        return f'Bot Telegram: permita que as notificações sejam enviadas para {tgram_user.title()}.'


class NotificationDirectorDisplay(NotificationManagerDisplay):

    def notification_dict(self, notification):
        return {
            "data": timezone.localtime(notification.timestamp).strftime('%d/%m/%Y'),
            "msg": self.get_notify_msg(notification),
            "receptor": notification.recipient.__str__(),
            "lida": notification.unread,
            "procedimento": notification.target.get_tipo_procedimento(),
            "link": notification.target.get_absolute_url()
        }

    def get_actor(self, notification):
        return notification.actor.get_full_name().title()

    def message_verb_incluiu(self, notification):
        actor = self.get_actor(notification)
        processo = notification.target.get_notification_label()
        notificado = notification.recipient.get_full_name().title()

        return f'{actor} {notification.verb} {notificado} no {processo}'

    def message_verb_notificou(self, notification):
        actor = self.get_actor(notification)
        ato = notification.action_object
        processo = notification.target.get_notification_label()
        notificado = notification.recipient.get_full_name().title()

        return f'{actor} {notification.verb} {notificado} sobre {ato} no {processo}'

    def message_verb_publicou(self, notification):
        actor = self.get_actor(notification)
        post = notification.target.truncate_titulo(50)

        return f'{actor} {notification.verb} o post: {post}'

    def message_verb_removeu(self, notification):
        actor = self.get_actor(notification)
        processo = notification.target.get_notification_label()
        notificado = notification.recipient.get_full_name().title()

        return f'{actor} {notification.verb} {notificado} do {processo}'

    def message_verb_solicitar(self, notification):
        gep_user = notification.actor.get_full_name().title()
        tgram_user = notification.description

        return f'{tgram_user.title()} solicitou ser notificado como {gep_user}'


class NotificationUserSentDisplay(NotificationDirectorDisplay):

    def get_actor(self, notification):
        return 'Você'


class SingleNotificationDisplay(NotificationUserDisplay):

    def __init__(self, notification):
        self.notification = notification

    def notification_dict(self):
        return {
            "msg": self.get_notify_msg(),
            "recipient_tgram": self.get_telegram()
        }

    def get_telegram(self):
        telegram = getattr(self.notification.recipient, 'telegramuser', False)
        permission = getattr(telegram, 'allowed', False)

        if telegram and permission:
            return telegram.chat_id
        return None

    def get_notify_msg(self):
        return super().get_notify_msg(self.notification)
