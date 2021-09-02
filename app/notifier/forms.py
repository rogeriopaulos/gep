# -*- coding: utf-8 -*-

from account.utils import UserModelChoiceField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout
from django import forms


class NotifiedUsersForm(forms.Form):

    usuarios = UserModelChoiceField(
            queryset=None,
            label="Usuários",
            widget=forms.widgets.SelectMultiple(attrs={'size': 90}),
            required=False
        )

    def __init__(self, queryset, *args, **kwargs):
        super(NotifiedUsersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('usuarios', css_class='col-md-12'),
                    css_class='col-md-10 col-md-offset-1 dp-colwhite'
                ), css_class='row'
            )
        )
        self.fields['usuarios'].queryset = queryset
