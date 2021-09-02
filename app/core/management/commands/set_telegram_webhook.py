# -*- coding: utf-8 -*-

import requests
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import BaseCommand
from django.urls import reverse


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        token = settings.TELEGRAM_TOKEN
        esisp_domain = Site.objects.last().domain
        path = reverse('notifier:connect_telegram_api')
        url = f"https://api.telegram.org/bot{token}/setWebhook?url=https://{esisp_domain}{path}"

        r = requests.get(url)
        print(r.json())
