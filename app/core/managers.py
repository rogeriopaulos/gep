# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q


class OfEmpresasManager(models.Manager):

    def get_empty_user_files(self, user):
        return self.filter(
            Q(autor=user) &
            Q(arquivo__exact='') &
            Q(conteudo__exact='') &
            Q(controlempresas__anulado=False)
        )


class OfInternoManager(models.Manager):

    def get_empty_user_files(self, user):
        return self.filter(Q(autor=user) & Q(arquivo__exact='') & Q(anulado=False))


class DocumentosManager(models.Manager):

    def get_empty_user_files(self, user):
        return self.filter(Q(autor=user) & Q(docs__exact='') & Q(anulado=False))
