from django.db import models

class Substancia(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Substância")
    formula = models.CharField(max_length=50, blank=True, null=True, verbose_name="Fórmula Química")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Substância"
        verbose_name_plural = "Substâncias"

# Modelo para temperaturas
class Temperatura(models.Model):
    valor_celsius = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Temperatura (°C)")

    def __str__(self):
        return f"{self.valor_celsius} °C"

    class Meta:
        verbose_name = "Temperatura"
        verbose_name_plural = "Temperaturas"

# Modelo para densidades
class Densidade(models.Model):
    substancia = models.ForeignKey(Substancia, on_delete=models.CASCADE, related_name="densidades")
    temperatura = models.ForeignKey(Temperatura, on_delete=models.CASCADE, related_name="densidades")
    concentracao_percentual = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Concentração (%)")
    densidade = models.DecimalField(max_digits=6, decimal_places=4, verbose_name="Densidade (g/cm³)")

    class Meta:
        unique_together = ('substancia', 'temperatura', 'concentracao_percentual')  # Evita duplicação
        verbose_name = "Densidade"
        verbose_name_plural = "Densidades"

    def __str__(self):
        return f"{self.substancia.nome} - {self.temperatura.valor_celsius} °C - {self.concentracao_percentual}%"


class UnidadeConversao:
    conversoes_concentracao = {
        'mg/L': 1e-3,
        'g/L': 1,
        'kg/L': 1e3,
        'mg/m³': 1e-6,
        'g/m³': 1e-3,
        'kg/m³': 1,
        'mol/L': 1,  # Assumindo que mol/L é equivalente a g/L para simplificação
        'ppm': 1e-3,
        '%': 10,
    }

    conversoes_vazao = {
        'L/s': 1,
        'L/min': 1 / 60,
        'L/h': 1 / 3600,
        'L/dia': 1 / 86400,
        'm³/s': 1000,
        'm³/min': 1000 / 60,
        'm³/h': 1000 / 3600,
        'm³/dia': 1000 / 86400,
    }

    @staticmethod
    def converter_concentracao(valor, unidade_origem, unidade_destino):
        fator_origem = UnidadeConversao.conversoes_concentracao.get(unidade_origem, 1)
        fator_destino = UnidadeConversao.conversoes_concentracao.get(unidade_destino, 1)
        return valor * (fator_origem / fator_destino)

    @staticmethod
    def converter_volume(valor, unidade_origem, unidade_destino):
        if unidade_origem == 'mL' and unidade_destino == 'L':
            return valor / 1000
        elif unidade_origem == 'L' and unidade_destino == 'mL':
            return valor * 1000
        return valor

    @staticmethod
    def converter_vazao(valor, unidade_origem, unidade_destino):
        fator_origem = UnidadeConversao.conversoes_vazao.get(unidade_origem, 1)
        fator_destino = UnidadeConversao.conversoes_vazao.get(unidade_destino, 1)
        return valor * (fator_origem / fator_destino)