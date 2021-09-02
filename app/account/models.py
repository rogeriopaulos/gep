# -*- coding: utf-8 -*-

from auditlog.registry import auditlog
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from guardian.shortcuts import get_objects_for_user, remove_perm

User = get_user_model()


class Orgao(models.Model):

    orgao = models.CharField('Órgão', max_length=255)
    sigla = models.CharField('Sigla', max_length=30, null=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name='permissões do orgão',
        blank=True,
        help_text='Informe os módulos que este orgão tem permissão de acesso.',
    )

    class Meta:
        verbose_name = '[NORMALIZAÇÃO] Órgão'
        verbose_name_plural = '[NORMALIZAÇÃO] Órgãos'
        permissions = (
            ('access_ADMINISTRATIVO', 'Acesso ao Módulo ADMINISTRATIVO'),
        )

    def __str__(self):
        return self.orgao

    def has_perm(self, perm):
        qs = Permission.objects.none()
        if '.' in perm:
            app_label, codename = perm.split('.')
            qs = self.permissions.all().filter(codename=codename, content_type__app_label=app_label)
        else:
            codename = perm
            qs = self.permissions.all().filter(codename=codename)
        if qs.count() == 1:
            return True
        return False


class Cargo(models.Model):

    orgao = models.ForeignKey(Orgao, on_delete=models.CASCADE, related_name='cargos')
    cargo = models.CharField('Cargo', max_length=255)

    class Meta:
        verbose_name = '[NORMALIZAÇÃO] Cargo'
        verbose_name_plural = '[NORMALIZAÇÃO] Cargos'

    def __str__(self):
        return f'{self.cargo}'


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nascimento = models.DateField('Data de nascimento', blank=True, null=True)
    orgao_link = models.ForeignKey(
        Orgao,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Instituição a qual está vinculado',
        null=True
    )
    cargo_link = models.ForeignKey(
        Cargo,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Cargo',
        null=True
    )
    lotacao = models.CharField('Unidade de lotação atual', max_length=50)
    funcao = models.CharField('Função que exerce', max_length=50, blank=True, null=True)
    matricula = models.CharField('Matrícula', max_length=15)
    cpf = models.CharField(
        'CPF',
        max_length=14,
        validators=[
            RegexValidator(
                regex=r'(^\d{3}\x2E\d{3}\x2E\d{3}\x2D\d{2}$)',
                message=r'O CPF informado deve ser no padrão "000.111.222-33".',
                code='CPF inválido',
            )],
        blank=True,
        null=True
    )
    identidade = models.CharField('Identidade', max_length=20, blank=True, null=True)
    org_identidade = models.CharField('Órgão Expedidor', max_length=10, blank=True, null=True)
    cel_funcional = models.CharField(
        'Celular funcional', max_length=15, blank=True,
        validators=[
            RegexValidator(
                regex=r'^\([1-9]{2}\) (?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$',
                message='O telefone informado deve ser no padrão \
                (DDD) NNNNN-NNNN.',
                code='Número inválido',
            )]
    )
    cel_pessoal = models.CharField(
        'Celular pessoal', max_length=15, blank=True,
        validators=[
            RegexValidator(
                regex=r'^\([1-9]{2}\) (?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$',
                message='O telefone informado deve ser no padrão \
                (DDD) NNNNN-NNNN.',
                code='Número inválido',
            )]
    )
    endereco = models.CharField('Endereço', max_length=200, blank=True, null=True)
    cep = models.CharField(
        'CEP', max_length=9, blank=True, null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{3}$',
                message='O CEP informado deve ser no padrão "00000-000".',
                code='CEP inválido',
            )]
    )
    alterar_senha = models.BooleanField("Forçar alteração de senha", default=False)
    subscritor = models.BooleanField("Pode subscrever documentos?", default=False)

    def __str__(self):
        return '{} {}'.format(self.user.first_name.upper(), self.user.last_name.upper())

    class Meta:
        verbose_name = 'Usuário GEP'
        verbose_name_plural = 'Usuários GEP'


def get_modules():
    return {
        'access_ADMINISTRATIVO': {
            'permissoes': [
                'adm.view_administrativo',
                'adm.add_administrativo',
                'adm.change_administrativo'
            ],
        },
    }


def get_modules_with_access(user):
    orgao = user.profile.orgao_link if user.profile.orgao_link else None
    if user.is_superuser or orgao is None:
        return []
    return [perm.codename for perm in orgao.permissions.all()]


@receiver(pre_save, sender=Profile)
def remove_processos_profile(sender, instance, **kwargs):
    if instance.pk is not None:
        current = instance
        previous = Profile.objects.get(pk=instance.pk)

        if previous.orgao_link != current.orgao_link:
            previous_user = previous.user
            modules = get_modules()
            modules_with_access = get_modules_with_access(previous_user)

            for module in set(modules) & set(modules_with_access):
                info = modules[module]
                qs = get_objects_for_user(
                    previous_user,
                    info['permissoes'],
                    accept_global_perms=False,
                    any_perm=True
                ).filter(orgao_processo=previous.orgao_link)

                if qs:
                    for perm in info['permissoes']:
                        remove_perm(perm, previous_user, qs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.is_superuser:
        instance.profile.save()


auditlog.register(Profile)
auditlog.register(User, exclude_fields=['last_login'])
