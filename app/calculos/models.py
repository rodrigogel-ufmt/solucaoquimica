from django.db import models

class Substancia(models.Model):
    id = models.AutoField(primary_key=True) 
    nome = models.CharField(max_length=100)  # Nome da substância
    formula = models.CharField(max_length=50)  # Fórmula química
    massa_molar = models.DecimalField(max_digits=10, decimal_places=5)  # Massa molar (g/mol)
    ppm_total = models.DecimalField(max_digits=10, decimal_places=4)  # PPM total da substância
    temperatura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Temperatura (ºC) opcional
    densidade = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)  # Densidade (g/mL)
    concentracao = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)  # Concentração (mol/L) opcional
    
    def __str__(self):
        return self.nome

    # Método para calcular a molaridade
    def calcular_molaridade(self):
        # return self.ppm_total / (self.massa_molecular * 1000)    
        return self.concentracao/100*self.densidade*self.ppm_total/self.massa_molecular

    def converter_para_mol_por_litro(self, quantidade):
        return quantidade / self.massa_molar

    def converter_concentracao(self, quantidade, unidade, fator_equivalencia=1):
        if unidade == 'g/L':
            return self.converter_para_mol_por_litro(quantidade)
        elif unidade == '%':
            return None
        elif unidade == 'ppm':
            return self.converter_para_mol_por_litro(quantidade / 1000)  # Converte mg/L para g/L
        elif unidade == 'mg/L':
            return self.converter_para_mol_por_litro(quantidade / 1000)
        elif unidade == 'N':
            return quantidade * fator_equivalencia  # Converte N para mol/L
        else:
            raise ValueError("Unidade não suportada.")

class UnidadeConversao:
    conversoes_concentracao = {
        'mg/L': 1,
        'g/L': 1e-3,
        'kg/L': 1e-6,
        'mg/m³': 1e3,
        'g/m³': 1,
        'kg/m³': 1e-3,
        'mol/L': 1,
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