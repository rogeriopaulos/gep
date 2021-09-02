# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class TelegramUser(models.Model):

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, unique=True)
    chat_id = models.CharField('Chat Id', max_length=15)
    allowed = models.BooleanField(default=False)
    chat_fullname = models.CharField('Chat Fullname', max_length=30, default=' ')

    def __str__(self):
        return f'{self.user}'

    def get_absolute_url(self):
        return reverse("notifier:allow_telegram")

    def get_tipo_procedimento(self):
        return 'Cadastro Telegram'

    def allow(self):
        self.allowed = True
        self.save()
