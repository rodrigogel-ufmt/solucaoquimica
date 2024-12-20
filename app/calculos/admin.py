from django.contrib import admin
from .models import Substancia, Temperatura, Densidade

@admin.register(Substancia)
class SubstanciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'formula')
    search_fields = ('nome', 'formula')

@admin.register(Temperatura)
class TemperaturaAdmin(admin.ModelAdmin):
    list_display = ('valor_celsius',)
    search_fields = ('valor_celsius',)

@admin.register(Densidade)
class DensidadeAdmin(admin.ModelAdmin):
    list_display = ('substancia', 'temperatura', 'concentracao_percentual', 'densidade')
    list_filter = ('substancia', 'temperatura')
    search_fields = ('substancia__nome', 'temperatura__valor_celsius')