from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('mistura/', views.mistura, name='mistura'),         # Rota para a funcionalidade de mistura de soluções
    path('diluicao/', views.diluicao, name='diluicao'),      # Rota para a funcionalidade de diluição de soluções
    path('conversao/', views.conversao, name='conversao'),   # Rota para a funcionalidade de conversão de unidades
    path('relatorio/', views.gerar_relatorio, name='relatorio'),  # Rota para geração de relatórios em PDF
    path('sobre-teorias/', views.sobre_teorias, name='sobre_teorias'),  # Rota para a página de teorias
]
