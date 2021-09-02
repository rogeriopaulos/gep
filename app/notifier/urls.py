from django.urls import path

from . import views

app_name = 'notifier'

urlpatterns = [
    path('processo/ato/adm/<int:model_pk>/', views.notifica_ato_adm, name='ato_adm'),
    path('processo/oficio/inter/<int:model_pk>/', views.notifica_oficio_empresa, name='oficio_empresa'),
]
