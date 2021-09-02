# -*- coding: utf-8 -*-

from django import forms


class UserModelChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return obj.get_full_name().title()


class UserExternalModelChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.get_full_name().title()} ({obj.profile.orgao_link.sigla})'


# tests
CARGOS = (
    ('cargo1', 'cargo1'),
    ('cargo2', 'cargo2'),
    ('cargo3', 'cargo3'),
    ('cargo4', 'cargo4'),
    ('cargo5', 'cargo5'),
    ('cargo6', 'cargo6'),
    ('cargo7', 'cargo7'),
    ('cargo8', 'cargo8'),
    ('cargo9', 'cargo9'),
    ('cargo10', 'cargo10'),
    ('cargo11', 'cargo11'),
)

INSTITUICOES = (
    ('orgao1', 'orgao1'),
    ('orgao2', 'orgao2'),
    ('orgao3', 'orgao3'),
    ('orgao4', 'orgao4'),
)
