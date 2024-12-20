from django import forms
from django.forms import formset_factory

from .models import Substancia

class MisturaForm(forms.Form):
    substancia = forms.ModelChoiceField(queryset=Substancia.objects.all().distinct(), label="Substância", to_field_name='nome')
    temperatura = forms.ChoiceField(label="Temperatura (°C)", choices=[])

class DilucaoForm(forms.Form):
    concentracao_inicial = forms.FloatField(label="Concentração Inicial")
    unidade_concentracao_inicial = forms.ChoiceField(
        label="Unidade da Concentração Inicial",
        choices=[('M', 'M'), ('g/L', 'g/L'), ('ppm', 'ppm'), ('%', '%')],
        initial='M'
    )
    volume_final = forms.FloatField(label="Volume Final")
    unidade_volume_final = forms.ChoiceField(
        label="Unidade do Volume Final",
        choices=[('mL', 'mL'), ('L', 'L')],
        initial='mL'
    )
    concentracao_final = forms.FloatField(label="Concentração Final")
    unidade_concentracao_final = forms.ChoiceField(
        label="Unidade da Concentração Final",
        choices=[('M', 'M'), ('g/L', 'g/L'), ('ppm', 'ppm')],
        initial='M'
    )

class ConversaoForm(forms.Form):
    valor = forms.FloatField(label="Valor")
    unidade_origem = forms.ChoiceField(choices=[
        ('mg/L', 'mg/L'),
        ('g/L', 'g/L'),
        ('kg/L', 'kg/L'),
        ('mg/m³', 'mg/m³'),
        ('g/m³', 'g/m³'),
        ('kg/m³', 'kg/m³'),
        ('L/s', 'L/s'),
        ('L/min', 'L/min'),
        ('L/h', 'L/h'),
        ('L/dia', 'L/dia'),
        ('m³/s', 'm³/s'),
        ('m³/min', 'm³/min'),
        ('m³/h', 'm³/h'),
        ('m³/dia', 'm³/dia'),
    ])
    unidade_destino = forms.ChoiceField(choices=[
        ('mg/L', 'mg/L'),
        ('g/L', 'g/L'),
        ('kg/L', 'kg/L'),
        ('mg/m³', 'mg/m³'),
        ('g/m³', 'g/m³'),
        ('kg/m³', 'kg/m³'),
        ('L/s', 'L/s'),
        ('L/min', 'L/min'),
        ('L/h', 'L/h'),
        ('L/dia', 'L/dia'),
        ('m³/s', 'm³/s'),
        ('m³/min', 'm³/min'),
        ('m³/h', 'm³/h'),
        ('m³/dia', 'm³/dia'),
    ])

class SolucaoForm(forms.Form):
    volume = forms.FloatField(label="Volume")
    unidade_volume = forms.ChoiceField(
        label="Unidade do Volume",
        choices=[('mL', 'mL'), ('L', 'L'), ('m³', 'm³'), ('gal', 'gal'), ('ft³', 'ft³'), ('in³', 'in³'), ('cm³', 'cm³'), ('mm³', 'mm³') ],
             initial='L')
    concentracao = forms.FloatField(label="Concentração")
    unidade_concentracao = forms.ChoiceField(
        label="Unidade da Concentração",
        choices=[('g/L', 'g/L'), ('mol/L', 'mol/L'), ('ppm', 'ppm'), ('N', 'N'), ('%', '%'), ('mg/L', 'mg/L') ],
             initial='mol/L')


SolucaoFormset = formset_factory(SolucaoForm, extra=1, min_num=1, validate_min=True)