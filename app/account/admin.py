# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission, User

from .forms import UserAdminForm, UserAdmminCreationForm
from .models import Cargo, Orgao, Profile


class UserAdmin(BaseUserAdmin):

    add_form = UserAdmminCreationForm
    add_fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        }),
    )
    form = UserAdminForm
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Informações Básicas', {
            'fields': ('first_name', 'last_name', 'last_login')
        }),
        ('Permissões', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'
            )
        }),
    )
    date_hierarchy = 'date_joined'
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_active', 'groups', 'is_staff')
    list_display = ('__str__', 'full_name', 'email', 'profile__cargo', 'get_orgao', 'date_joined', 'is_active')
    ordering = ('-date_joined',)

    def full_name(self, obj):
        return obj.get_full_name().upper()

    full_name.short_description = 'Nome'

    def profile__cargo(self, obj):
        return obj.profile.cargo_link

    profile__cargo.short_description = 'Cargo'

    def get_orgao(self, instance):
        return instance.profile.orgao_link.sigla if instance.profile.orgao_link else None

    get_orgao.short_description = 'Órgão'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):

    date_hierarchy = 'user__date_joined'
    search_fields = ('user__first_name', 'user__last_name', 'funcao')
    list_display = ('get_username', 'full_name', 'matricula', 'get_orgao', 'cargo_link', 'get_cadastro', 'get_active')
    list_filter = ('user__is_active', 'cargo_link__cargo', 'subscritor')
    permission = 'account.view_profile'
    ordering = ('-user__date_joined',)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser and request.user.has_perm(self.permission):
            return [f.name for f in self.model._meta.fields]
        return super(ProfileAdmin, self).get_readonly_fields(request, obj=obj)

    def get_username(self, obj):
        return obj.user.username

    get_username.admin_order_field = 'user__username'
    get_username.short_description = 'Usuário'

    def full_name(self, obj):
        return obj.user.get_full_name().upper()

    full_name.admin_order_field = 'user__first_name'
    full_name.short_description = 'Nome'

    def get_cadastro(self, obj):
        return obj.user.date_joined

    get_cadastro.admin_order_field = 'user__date_joined'
    get_cadastro.short_description = 'Cadastro'

    def get_orgao(self, obj):
        return obj.orgao_link.sigla if obj.orgao_link else None

    get_orgao.short_description = 'Órgão'

    def get_active(self, obj):
        if obj.user.is_active:
            return 'Sim'
        else:
            return 'Não'

    get_active.short_description = 'Ativo'


admin.site.register(Profile, ProfileAdmin)


class CargoAdmin(admin.ModelAdmin):

    list_display = ('str_name', 'orgao', 'cargo')
    list_filter = ('orgao',)

    def str_name(self, obj):
        return f'{obj.cargo} ({obj.orgao})'

    str_name.admin_order_field = 'cargo'
    str_name.short_description = 'Cargos'


admin.site.register(Cargo, CargoAdmin)


class OrgaoAdmin(admin.ModelAdmin):

    list_display = ('orgao', 'sigla')

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['permissions'].queryset = Permission.objects.filter(
            content_type__app_label='account', content_type__model='orgao', codename__istartswith='access_')
        return super().render_change_form(request, context, *args, **kwargs)


admin.site.register(Orgao, OrgaoAdmin)
