# -*- coding: utf-8 -*-

from account import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView
from django.urls import path

app_name = "account"
urlpatterns = [
    path('atos/json/', views.atos_json, name='atos_json'),
    path('atos/pendentes/json/', views.atos_pendentes_json, name='atos_pendentes_json'),
    path('minha-conta/', views.minha_conta, name='minha_conta'),
    path('login/', LoginView.as_view(template_name='componentes/singles/core/Home.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='componentes/singles/core/Home.html'), name='logout'),
    path('painel/', views.painel_view, name='painel'),
    path('painel/notificacoes/', views.notificacoes, name='notificacoes'),
    path('painel/notificacoes/enviadas', views.notifications_sent, name='notifications_sent'),
    path('processos/json/', views.processos_criados_json, name='processos_criados_json'),
    path('processos/vinculados/json/', views.processos_vinculados_json, name='processos_vinculados_json'),
    path('recuperar-senha/', views.PasswordResetCustomView.as_view(), name='password_reset'),
    path('notificacao/lida/', views.notificacao_lida, name='notificacao_lida'),
    path('notificacaoes/lidas/', views.set_all_notifications_read, name='set_all_notifications_read'),
    path('notificacaoes-recebidas/json/', views.notifications_receive_json, name='notifications_receive_json'),
    path('notificacaoes-enviadas/json/', views.notifications_sent_json, name='notifications_sent_json'),
    path('recuperar-senha/confirma/<uidb64>/<token>/', views.PasswordResetConfirmCustomView.as_view(), name='password_reset_confirm'),  # noqa: E501
    path('recuperar-senha/solicitacao/concluida/', PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),  # noqa: E501
]
