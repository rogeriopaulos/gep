# -*- coding: utf-8 -*-

from account.models import Profile
from account.utils import UserExternalModelChoiceField, UserModelChoiceField
from core.models import VinculoProcesso
from core.validators import file_validator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout
from django import forms
from django.forms import ModelForm, widgets


class OfEmpresasCoreUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(OfEmpresasCoreUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Field('autoridade'),
                Field('confirmacao'),
                Field('nome_confirm', css_class='dp-uppercase'),
                css_class='col-md-4 col-md-offset-4 dp-colwhite'
            )
        )

    class Meta:
        fields = ['confirmacao', 'nome_confirm', 'autoridade']


class MidiaCoreForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MidiaCoreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Field('destino', css_class='dp-uppercase'),
                Field('solicitante', css_class='dp-uppercase'),
                Field('oforigem', css_class='dp-uppercase'),
                Field('tipo_gravacao_link'),
                Field('docs'),
                Field('descricao'),
                css_class='col-md-4 col-md-offset-4 dp-colwhite'
            )
        )
        self.fields['docs'].validators.append(file_validator())

    class Meta:
        fields = ['destino', 'solicitante', 'oforigem', 'tipo_gravacao_link', 'docs', 'descricao']


class OfInternoCoreForm(ModelForm):

    autoridade = forms.ModelChoiceField(
        queryset=Profile.objects
        .select_related('user')
        .filter(subscritor=True, user__is_active=True),
        error_messages={'invalid_choice': 'Usuário não encontrado.'},
        label='Autoridade que subscreve'
    )

    def __init__(self, *args, **kwargs):
        orgao_pk = kwargs.pop('orgao_pk')

        super(OfInternoCoreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Field('destino', css_class='dp-uppercase'),
                Field('conteudo', css_class='dp-select'),
                Field('outros', css_class='dp-uppercase dp-outros'),
                Field('autoridade', css_class='dp-uppercase'),
                Field('descricao'),
                css_class='col-md-4 col-md-offset-4 dp-colwhite'
            )
        )
        self.fields['autoridade'].queryset = self.fields['autoridade'].queryset.filter(orgao_link__pk=orgao_pk)

    class Meta:
        fields = ['destino', 'conteudo', 'outros', 'autoridade', 'descricao']


class OfInternoCoreUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(OfInternoCoreUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Field('confirmacao'),
                Field('nome_confirm', css_class='dp-uppercase'),
                Field('data_envio', css_class='dp-data'),
                Field('descricao'),
                css_class='col-md-4 col-md-offset-4 dp-colwhite'
            )
        )

    class Meta:
        fields = ['data_envio', 'confirmacao', 'nome_confirm', 'descricao']


class OfExternoCoreForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(OfExternoCoreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Field('num_oficio'),
                Field('origem', css_class='dp-uppercase'),
                Field('conteudo', css_class='dp-select'),
                Field('outros', css_class='dp-uppercase dp-outros'),
                Field('data_recebimento', css_class='dp-data'),
                Field('nome_recebimento', css_class='dp-uppercase'),
                Field('arquivo'),
                Field('descricao'),
                css_class='col-md-4 col-md-offset-4 dp-colwhite'
            )
        )
        self.fields['arquivo'].validators.append(file_validator())

    class Meta:
        fields = ['num_oficio', 'origem', 'conteudo', 'outros', 'arquivo',
                  'data_recebimento', 'nome_recebimento', 'descricao']


class UserMultipleChoiceForm(forms.Form):

    usuarios = UserModelChoiceField(
        queryset=None,
        label="Usuários",
        widget=widgets.SelectMultiple(attrs={'size': 90})
    )

    def __init__(self, queryset=None, *args, **kwargs):
        super(UserMultipleChoiceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field('usuarios', css_class='col-md-12'), css_class='dp-colwhite'),
                css_class='row'
            )

        )
        self.fields['usuarios'].queryset = queryset


class UserExternalMultipleChoiceForm(forms.Form):

    usuarios = UserExternalModelChoiceField(
        queryset=None,
        label="Usuários",
        widget=widgets.SelectMultiple(attrs={'size': 90})
    )

    def __init__(self, queryset=None, *args, **kwargs):
        super(UserExternalMultipleChoiceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field('usuarios', css_class='col-md-12'), css_class='dp-colwhite'),
                css_class='row'
            )

        )
        self.fields['usuarios'].queryset = queryset


class PermforUsersForm(forms.Form):

    username = forms.CharField(label='Usuário',)
    visualizar = forms.BooleanField(label='Somente vizualizar', required=False)
    adicionar = forms.BooleanField(label='Adicionar novos atos', required=False)
    alterar = forms.BooleanField(label='Editar atos existentes', required=False)

    def __init__(self, *args, **kwargs):
        super(PermforUsersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_class = 'form-inline'
        self.helper.template = 'bootstrap/table_inline_formset.html'
        self.helper.layout = Layout(
            Div(
                Div('username', css_class='col-sm-2'),
                Div('visualizar', css_class='col-sm-3'),
                Div('adicionar', css_class='col-sm-4'),
                Div('alterar', css_class='col-sm-3'),
                css_class='row'
            )
        )

        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['size'] = '10'


PermUsersFormset = forms.formset_factory(PermforUsersForm, extra=0, can_delete=False)


class VinculoProcessoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        orgao_pk = kwargs.pop('orgao_pk')

        super(VinculoProcessoForm, self).__init__(*args, **kwargs)
        self.fields['processo_b'].queryset = self.fields['processo_b'].queryset.filter(orgao_processo__pk=orgao_pk)

    class Meta:
        model = VinculoProcesso
        fields = ['processo_b', 'motivo_vinculo']
