# -*- coding: utf-8 -*-


def count_notifications(request):
    if not request.user.is_anonymous:
        count = request.user.notifications.unread().count()
    else:
        count = 0
    return {'unread_notifications': count}
