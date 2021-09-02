# -*- coding: utf-8 -*-

from django.urls import path
from django.views.generic import TemplateView

from . import views

arquivado_template = 'componentes/singles/core/Arquivado.html'
app_name = "core"

urlpatterns = [
    path('', views.home_view, name='home'),
    path('arquivado/', TemplateView.as_view(template_name=arquivado_template), name='arquivado'),
]
