# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.core import serializers
from django.db import OperationalError
from notifications.signals import notify

from .helper import NotificationUserDisplay
from .utils import send_to_email_users


@shared_task(bind=True)
def notificar(self, context, test=False):
    try:
        deserialized_actor = [_ for _ in serializers.deserialize('json', context['actor'])][0]
        actor = deserialized_actor.object
    except AttributeError:  # pragma: no cover
        actor = None
    try:
        deserialized_target = [_ for _ in serializers.deserialize('json', context['target'])][0]
        target = deserialized_target.object
    except AttributeError:  # pragma: no cover
        target = None
    try:
        deserialized_act_object = [_ for _ in serializers.deserialize('json', context['action_object'])][0]
        action_object = deserialized_act_object.object
    except AttributeError:  # pragma: no cover
        action_object = None

    users = [_.object for _ in serializers.deserialize('json', context['users'])]

    notifications = notify.send(
        actor,
        recipient=users,
        verb=context['verb'],
        target=target,
        action_object=action_object,
        description=context['description']
    )

    nt = NotificationUserDisplay(notifications[0][1])

    user_emails = [_.object.email for _ in serializers.deserialize('json', context['users'])]

    email_context = {
        'msg': nt.get_notify_msg(nt.notifications[0]),
        'user_emails': user_emails,
        'unsent_notices': serializers.serialize('json', nt.notifications)
    }

    if not test:  # pragma: no cover
        on_email.delay(email_context)


@shared_task(bind=True)
def on_email(self, context, test=False):
    context['unsent_notices'] = [_.object for _ in serializers.deserialize('json', context['unsent_notices'])]

    try:
        if not test:  # pragma: no cover
            send_to_email_users(context)
    except OperationalError as exc:   # pragma: no cover
        raise self.retry(exc=exc)
