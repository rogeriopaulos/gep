# -*- coding: utf-8 -*-

from adm import views
from django.urls import path

app_name = "adm"

urlpatterns = [
    # Processo
    path('instaurar/', views.criar_processo_adm, name='criar_processo_adm'),
    path('listar/', views.listar_adm, name='listar_adm'),
    path('listar/ajax/', views.processos_adm_ajax, name='processos_adm_ajax'),
    path('<int:pk>/detalhes/', views.detalhe_processo_adm, name='detalhe_processo_adm'),
    path('<int:pk>/editar/', views.editar_processo_adm, name='editar_processo_adm'),
    path('<int:pk>/extrato_administrativo.pdf', views.extrato_pdf_adm, name='extrato_pdf_adm'),
    path('vincular_processos/<int:pk>/', views.vincular_processos, name='vincular_processos'),
    # Ato: Expedir ofício
    path('<int:pk>/expedir-oficio/<int:tipo_ato>/adicionar/', views.add_ofinterno_adm, name='add_ofinterno_adm'),
    path('expedir-oficio/<int:pk>/editar/', views.editar_ofinterno_adm, name='editar_ofinterno_adm'),
    path('expedir-oficio/<int:pk>/editar_arquivo/', views.editar_ofinterno_arq_adm, name='editar_ofinterno_arq_adm'),  # noqa: E501
    path('expedir-oficio/<int:pk>/confirmacao/', views.editar_confirmacao_adm, name='editar_confirmacao_adm'),
    path('expedir-oficio/<int:pk>/data-envio/', views.editar_dataenvio_adm, name='editar_dataenvio_adm'),
    # Ato: Ofício Recebido
    path('<int:pk>/oficio-externo/<int:tipo_ato>/adicionar/', views.add_ofexterno_adm, name='add_ofexterno_adm'),
    path('oficio-externo/<int:pk>/editar/', views.editar_ofexterno_adm, name='editar_ofexterno_adm'),
    # Ato: Ofícios para empresas
    path('<int:pk>/oficio-empresas/<int:tipo_ato>/adicionar/', views.add_ofempresas, name='add_ofempresas'),
    path('oficio-empresas/<int:pk>/arquivo/upload/', views.ofempresas_upload_arquivo, name='ofempresas_upload_arquivo'),
    path('oficio-empresas/<int:pk>/confirmar/', views.ofempresas_confirmar, name='ofempresas_confirmar'),
    path('oficio-empresas/<int:pk>/editar/', views.ofempresas_editar, name='ofempresas_editar'),
    # Ato: Despacho
    path('<int:pk>/despacho/add/<int:tipo_ato>/', views.add_despacho_adm, name='add_despacho_adm'),
    path('despacho/<int:pk>/editar/', views.editar_despacho_adm, name='editar_despacho_adm'),
    # Ato: Status
    path('<int:pk>/status/add/<int:tipo_ato>/', views.add_status_adm, name='add_status_adm'),
    path('status/<int:pk>/editar/', views.editar_status_adm, name='editar_status_adm'),
    # Ato: Mídia
    path('<int:pk>/gravacao/add/<int:tipo_ato>/', views.add_gravacao_adm, name='add_gravacao_adm'),
    path('<int:pk>/documento/add/<int:tipo_ato>/', views.add_documento_adm, name='add_documento_adm'),
    # Ato: Documentos Gerais
    path('documento/<int:pk>/editar/', views.editar_documento_adm, name='editar_documento_adm'),
    # Ato: Seleção & Permissão de usuários
    path('<int:pk>/selecionar_user_permitidos/', views.select_user_adm, name='select_user_adm'),
    path('<int:pk>/selecionar_user_externos_permitidos/', views.add_external_users_adm, name='add_external_users_adm'),
    path('<int:pk>/perm_user/', views.select_perm_adm, name='select_perm_adm'),
    # Ato: Ações
    path('anular/<int:pk>', views.anular_ato, name='anular_ato'),
]
