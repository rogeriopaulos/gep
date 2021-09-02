# -*- coding: utf-8 -*-

from account.models import Profile
from adm.models import (
    Administrativo,
    ControlEmpresas,
    DespachoAdm,
    DocumentosGeraisAdm,
    MidiaAdm,
    OfEmpresas,
    OficioExternoAdm,
    OficioInternoAdm,
    StatusAdm
)
from core.forms import MidiaCoreForm, OfEmpresasCoreUpdateForm, OfExternoCoreForm, OfInternoCoreUpdateForm
from core.validators import file_validator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout
from django.forms import ModelChoiceField, ModelForm, ValidationError, inlineformset_factory


class AdministrativoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdministrativoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Div(
                Field('assunto_adm', css_class='dp-select'),
                Field('outro', css_class='dp-uppercase dp-outros'),
                Field('destino_adm', css_class="dp-uppercase"),
                Field('oficiante', css_class="dp-uppercase"),
                Field('email'),
                Field('fone', css_class="dp-fone", placeholder="(DDD)NNNNN-NNNN"),
                Field('arquivo'),
                Field('observacao'),
                css_class="col-md-4",
            ),
        )
        self.fields['arquivo'].validators.append(file_validator())

    class Meta:
        model = Administrativo
        fields = ['assunto_adm', 'outro', 'destino_adm', 'oficiante', 'email',
                  'fone', 'observacao', 'arquivo']

    def clean(self):
        cleaned_data = super(AdministrativoForm, self).clean()
        assunto = cleaned_data.get('assunto_adm')
        outro = cleaned_data.get('outro')
        if assunto.assunto == 'OUTRO(S)' and len(outro) == 0:
            raise ValidationError("O campo 'Outro(s)' deve ser preenchido")


class AdministrativoUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdministrativoUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Div(
                Field('assunto_adm', css_class='dp-select'),
                Field('outro', css_class='dp-uppercase dp-outros'),
                Field('destino_adm', css_class="dp-uppercase"),
                Field('oficiante', css_class="dp-uppercase"),
                Field('email'),
                Field('fone', css_class="dp-fone", placeholder="(DDD)NNNNN-NNNN"),
                Field('arquivo'),
                Field('observacao'),
                Field('arquivar'),
                css_class="col-md-4",
            ),
        )

    class Meta:
        model = Administrativo
        fields = ['assunto_adm', 'outro', 'destino_adm', 'oficiante', 'email',
                  'fone', 'observacao', 'arquivo', 'arquivar']

    def clean(self):
        cleaned_data = super(AdministrativoUpdateForm, self).clean()
        assunto = cleaned_data.get('assunto_adm')
        outro = cleaned_data.get('outro')
        if assunto.assunto == 'OUTRO(S)' and len(outro) == 0:
            raise ValidationError("O campo 'Outro(s)' deve ser preenchido")


class DespachoAdmForm(ModelForm):

    class Meta:
        model = DespachoAdm
        exclude = ['autor', 'modificador', 'processo', 'tipo_ato', 'observacao']


class StatusAdmForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(StatusAdmForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.error_text_inline = False
        self.helper.layout = Layout(
            Div(
                Field('localizacao', css_class="dp-select"),
                Field('outros', css_class="dp-uppercase dp-outros"),
                Field('situacao'),
                Field('descricao'),
                css_class='col-md-4 col-md-offset-4 dp-colwhite'
            ),
        )

    class Meta:
        model = StatusAdm
        fields = ['localizacao', 'situacao', 'outros', 'descricao']


class OficioInternoAdmForm(ModelForm):

    autoridade = ModelChoiceField(
        queryset=Profile.objects.select_related('user').filter(subscritor=True, user__is_active=True),
        error_messages={'invalid_choice': 'Usuário não encontrado.'},
        label='Autoridade que subscreve'
    )

    def __init__(self, *args, **kwargs):
        orgao_pk = kwargs.pop('orgao_pk')

        super(OficioInternoAdmForm, self).__init__(*args, **kwargs)
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
        model = OficioInternoAdm
        fields = ['destino', 'conteudo', 'outros', 'autoridade', 'descricao']


class OfInternoAdmUpdateForm(OfInternoCoreUpdateForm):

    autoridade = ModelChoiceField(
        queryset=Profile.objects.select_related('user').filter(subscritor=True, user__is_active=True),
        error_messages={'invalid_choice': 'Usuário não encontrado.'},
        label='Autoridade que subscreve'
    )

    def __init__(self, *args, **kwargs):
        super(OfInternoAdmUpdateForm, self).__init__(*args, **kwargs)
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

    class Meta:
        model = OficioInternoAdm
        fields = ['destino', 'conteudo', 'outros', 'autoridade', 'descricao']


class OficioExternoAdmForm(OfExternoCoreForm):

    class Meta(OfExternoCoreForm.Meta):
        model = OficioExternoAdm


class MidiaAdmForm(MidiaCoreForm):

    class Meta(MidiaCoreForm.Meta):
        model = MidiaAdm


class DocumentoAdmForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(DocumentoAdmForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Field('nome_doc'),
                Field('documento'),
                Field('descricao'),
                css_class='col-md-4 col-md-offset-4 dp-colwhite'
            )
        )
        self.fields['documento'].validators.append(file_validator())

    class Meta:
        model = DocumentosGeraisAdm
        fields = ['documento', 'descricao', 'nome_doc']


class ControlEmpresasForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ControlEmpresasForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('assunto', placeholder="Ex: Interceptação/Quebra de Dados"),
            Field('descricao')
        )

    class Meta:
        model = ControlEmpresas
        exclude = ['autor', 'modificador', 'tipo_ato', 'processo']


class OfEmpresasForm(ModelForm):

    autoridade = ModelChoiceField(
        queryset=Profile.objects.select_related('user').filter(subscritor=True, user__is_active=True),
        error_messages={'invalid_choice': 'Usuário não encontrado.'},
    )

    class Meta:
        model = OfEmpresas
        exclude = ['autor', 'modificador', 'criacao', 'alteracao', 'num_oficio']

    def __init__(self, *args, **kwargs):
        orgao_pk = kwargs.pop('orgao_pk')

        super(OfEmpresasForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['outros'].widget.attrs['placeholder'] = 'Empresa não listada'
        self.fields['outros'].widget.attrs['class'] = 'form-control dp-outros'
        self.fields['autoridade'].widget.attrs['class'] = 'form-control dp-autoridade'
        self.fields['autoridade'].queryset = self.fields['autoridade'].queryset.filter(orgao_link__pk=orgao_pk)
        self.fields['empresa'].widget.attrs['class'] = 'form-control dp-select'


OfEmpresasFormset = inlineformset_factory(
    ControlEmpresas,
    OfEmpresas,
    form=OfEmpresasForm,
    extra=1,
    fields=('empresa', 'outros', 'num_oficio', 'autoridade')
)


class OfEmpresasUpdateForm(OfEmpresasCoreUpdateForm):

    class Meta(OfEmpresasCoreUpdateForm.Meta):
        model = OfEmpresas
