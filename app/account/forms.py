# -*- coding: utf-8 -*-

from core.validators import validate_CPF
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import DateInput, EmailInput, TextInput

from .models import Profile


class UserAdmminCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']


class UserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': TextInput(attrs={"placeholder": "Digite um nome de usuário"}),
            'first_name': TextInput(attrs={"placeholder": "Digite seu primeiro nome", "required": True}),
            'last_name': TextInput(attrs={"placeholder": "Digite seu último nome"}),
            'email': EmailInput(attrs={"placeholder": "E-mail - Atenção para o domínio"}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe um usuário com este e-mail.')
        return email


class ProfileForm(forms.ModelForm):

    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        required=True,
        validators=[validate_CPF]
    )

    class Meta:
        model = Profile
        exclude = ['user', 'orgao', 'cargo']
        widgets = {
            'nascimento': DateInput(attrs={"type": "date"}),
            'cpf': TextInput(attrs={"placeholder": "Apenas números"}),
            'identidade': TextInput(attrs={"placeholder": "RG"}),
            'org_identidade': TextInput(attrs={"placeholder": "Sigla - Ex: SSP-PI..."}),
            'lotacao': TextInput(attrs={"placeholder": "Unidade de lotação"}),
            'funcao': TextInput(attrs={"placeholder": "Função que exerce atualmente"}),
            'matricula': TextInput(attrs={"placeholder": "Digite sua matrícula"}),
            'cel_funcional': TextInput(attrs={"placeholder": "Digite o número com o DDD"}),
            'cel_pessoal': TextInput(attrs={"placeholder": "Digite o número com o DDD"}),
            'endereco': TextInput(attrs={
                "placeholder":
                "Logradouro (Rua, Av...), nº, Conj., bairro, cidade, estado",
            }),
            'cep': TextInput(attrs={"placeholder": "Apenas números"}),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['org_identidade'].widget.attrs['class'] = 'dp-uppercase'
        self.fields['lotacao'].widget.attrs['class'] = 'dp-uppercase'
        self.fields['funcao'].widget.attrs['class'] = 'dp-uppercase'


class UserEditForm(forms.ModelForm):

    first_name = forms.CharField(label='Primeiro nome', max_length=30, required=True)
    last_name = forms.CharField(label='Sobrenome', max_length=30, required=True)
    email = forms.EmailField(label='E-mail', max_length=254, required=True)

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['required'] = 'required'
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.render_required_fields = True
        self.helper.form_style = 'inline'
        self.helper.layout = Layout(
            Div(
                Field('first_name', css_class='dp-uppercase'),
                css_class='col-md-2'
            ),
            Div(
                Field('last_name', css_class='dp-uppercase'),
                css_class='col-md-5'
            ),
            Div(
                Field('email'),
                css_class='col-md-5'
            )
        )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        consulta = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if consulta.exists():
            raise forms.ValidationError('Já existe um usuário com este e-mail.')
        return email


class ProfileEditForm(forms.ModelForm):

    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        required=True,
        validators=[validate_CPF]
    )

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.render_required_fields = True
        self.helper.layout = Layout(
            Div(
                Field('nascimento', css_class='dp-data'),
                css_class='col-md-3'
            ),
            Div(
                Field('cpf', placeholder='Digite apenas números'),
                css_class='col-md-3'
            ),
            Div(
                Field('identidade', placeholder='Digite apenas números'),
                css_class='col-md-3'
            ),
            Div(
                Field(
                    'org_identidade',
                    placeholder='Sigla do órgão',
                    css_class='dp-uppercase'
                ),
                css_class='col-md-3'
            ),
            Div(
                Field('matricula', placeholder='Digite apenas números'),
                css_class='col-md-4'
            ),
            Div(
                Field('lotacao', css_class='dp-uppercase'),
                css_class='col-md-4'
            ),
            Div(
                Field('funcao', css_class='dp-uppercase'),
                css_class='col-md-4'
            ),
            Div(
                Field('cel_pessoal', placeholder='Digite apenas números'),
                css_class='col-md-6'
            ),
            Div(
                Field('cel_funcional', placeholder='Digite apenas números'),
                css_class='col-md-6'
            ),
            Div(
                Field('endereco'),
                css_class='col-md-10'
            ),
            Div(
                Field('cep', placeholder='Digite apenas números'),
                css_class='col-md-2'
            ),
        )

    class Meta:
        model = Profile
        fields = ['nascimento', 'lotacao', 'funcao', 'matricula', 'cpf', 'cep',
                  'identidade', 'org_identidade', 'cel_funcional', 'endereco',
                  'cel_pessoal']
