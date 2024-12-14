from django.shortcuts import render
from django.http import HttpResponse
from .forms import MisturaForm, DilucaoForm, ConversaoForm, SolucaoForm, SolucaoFormset
from django.forms import formset_factory
from reportlab.pdfgen import canvas
from .models import UnidadeConversao


def index(request):
    return render(request, 'calculos/index.html')

from django.forms import formset_factory
from django.shortcuts import render
from .forms import SolucaoForm

def mistura(request):
    # Define o formset para múltiplas entradas de solução
    SolucaoFormset = formset_factory(SolucaoForm, extra=1)
    formset = SolucaoFormset()  # Instanciando um formset vazio inicialmente
    resultado = None

    # Configurações fixas
    temperatura = 20  # Temperatura fixa em °C
    massa_molar_h2so4 = 98.08  # Massa molar do Ácido Sulfúrico (H2SO4)

    if request.method == 'POST':
        formset = SolucaoFormset(request.POST)  # Preenchendo o formset com os dados do POST
        if formset.is_valid():
            total_volume = 0
            concentracao_molar_acumulada = 0

            # Processar cada formulário individualmente
            for form in formset:
                if form.cleaned_data:  # Garantir que os dados foram preenchidos
                    volume = form.cleaned_data['volume']
                    concentracao = form.cleaned_data['concentracao']
                    unidade_concentracao = form.cleaned_data['unidade_concentracao']
                    unidade_volume = form.cleaned_data['unidade_volume']
                    
                    # Conversão da concentração para mol/L
                    if unidade_concentracao == 'g/L':
                        concentracao_mol_l = concentracao / massa_molar_h2so4
                    elif unidade_concentracao == 'mol/L':
                        concentracao_mol_l = concentracao
                    elif unidade_concentracao == 'ppm':
                        concentracao_mol_l = (concentracao / 1000) / massa_molar_h2so4
                    elif unidade_concentracao == '%':
                        concentracao_mol_l = (concentracao * 10) / massa_molar_h2so4
                    else:
                        concentracao_mol_l = 0  # Caso unidade não seja reconhecida

                    total_volume += volume
                    concentracao_molar_acumulada += concentracao_mol_l * volume

            # Cálculo da concentração molar resultante, evitando divisão por zero
            if total_volume > 0:
                concentracao_resultante_mol_l = concentracao_molar_acumulada / total_volume
            else:
                concentracao_resultante_mol_l = 0

            # Resultado final
            resultado = {
                'volume_total': total_volume,
                'concentracao_molar': concentracao_resultante_mol_l,
                'temperatura': temperatura,
                'densidade': None,  # Pode adicionar lógica para calcular a densidade se necessário
            }

    return render(request, 'calculos/mistura.html', {'formset': formset, 'resultado': resultado})

# def diluicao(request):
#     form = DilucaoForm()
#     resultado = None
#     explicacao = None

#     if request.method == 'POST':
#         form = DilucaoForm(request.POST)
#         if form.is_valid():
#             c1 = form.cleaned_data['concentracao_inicial']
#             v2 = form.cleaned_data['volume_final']
#             c2 = form.cleaned_data['concentracao_final']

#             # Fórmula: C₁V₁ = C₂V₂
#             v1 = (c2 * v2) / c1  # Volume inicial necessário
#             volume_solvente = v2 - v1  # Volume de solvente a ser adicionado

#             resultado = {
#                 'volume_inicial': v1,
#                 'volume_solvente': volume_solvente,
#                 'volume_final': v2,
#             }

#             explicacao = (
#                 f"Para realizar a diluição, aplicamos a fórmula C₁V₁ = C₂V₂.\n"
#                 f"Com os valores fornecidos:\n"
#                 f"- Concentração inicial (C₁): {c1} M\n"
#                 f"- Volume final desejado (V₂): {v2} mL\n"
#                 f"- Concentração final desejada (C₂): {c2} M\n\n"
#                 f"Passos do cálculo:\n"
#                 f"1. Multiplicamos a concentração final (C₂) pelo volume final (V₂):\n"
#                 f"   {c2} M x {v2} mL = {c2 * v2:.2f} mL*M\n"
#                 f"2. Dividimos pelo valor da concentração inicial (C₁):\n"
#                 f"   ({c2 * v2:.2f} mL*M) / {c1} M = {v1:.2f} mL\n"
#                 f"3. Subtraímos o volume inicial (V₁) do volume final (V₂) para obter o volume de solvente:\n"
#                 f"   {v2} mL - {v1:.2f} mL = {volume_solvente:.2f} mL\n\n"
#                 f"O volume de solução inicial necessário é {v1:.2f} mL e o volume de solvente a ser adicionado é {volume_solvente:.2f} mL."
#             )

#     return render(request, 'calculos/diluicao.html', {'form': form, 'resultado': resultado, 'explicacao': explicacao})

def diluicao(request):
    form = DilucaoForm()
    resultado = None
    explicacao = None

    if request.method == 'POST':
        form = DilucaoForm(request.POST)
        if form.is_valid():
            # Dados do formulário
            c1 = form.cleaned_data['concentracao_inicial']
            unidade_c1 = form.cleaned_data['unidade_concentracao_inicial']
            v2 = form.cleaned_data['volume_final']
            unidade_v2 = form.cleaned_data['unidade_volume_final']
            c2 = form.cleaned_data['concentracao_final']
            unidade_c2 = form.cleaned_data['unidade_concentracao_final']

            # ** Conversão das Unidades **
            c1 = UnidadeConversao.converter_concentracao(c1, unidade_c1, 'mol/L')
            c2 = UnidadeConversao.converter_concentracao(c2, unidade_c2, 'mol/L')
            v2 = UnidadeConversao.converter_volume(v2, unidade_v2, 'L')

            # ** Realização do Cálculo **
            if c1 == 0:
                explicacao = "A concentração inicial não pode ser zero."
            else:
                # Fórmula: C₁V₁ = C₂V₂
                v1 = (c2 * v2) / c1  # Volume inicial necessário em litros
                volume_solvente = v2 - v1  # Volume de solvente em litros

                # Resultados em mililitros para exibição
                resultado = {
                    'volume_inicial': v1,  # Converter para mL
                }

                # Explicação detalhada
                explicacao = None

    return render(request, 'calculos/diluicao.html', {'form': form, 'resultado': resultado, 'explicacao': explicacao})

def conversao(request):
    form = ConversaoForm()
    resultado = None
    explicacao = None

    if request.method == 'POST':
        form = ConversaoForm(request.POST)
        if form.is_valid():
            valor = form.cleaned_data['valor']
            unidade_origem = form.cleaned_data['unidade_origem']
            unidade_destino = form.cleaned_data['unidade_destino']

            # Conversão de Unidades de Concentração
            if unidade_origem in UnidadeConversao.conversoes_concentracao and unidade_destino in UnidadeConversao.conversoes_concentracao:
                resultado = UnidadeConversao.converter_concentracao(valor, unidade_origem, unidade_destino)
                explicacao = (
                    f"Conversão de {unidade_origem} para {unidade_destino}:\n"
                    f"Resultado: {resultado:.6f} {unidade_destino}"
                )

            # Conversão de Unidades de Vazão
            elif unidade_origem in UnidadeConversao.conversoes_vazao and unidade_destino in UnidadeConversao.conversoes_vazao:
                resultado = UnidadeConversao.converter_vazao(valor, unidade_origem, unidade_destino)
                explicacao = (
                    f"Conversão de {unidade_origem} para {unidade_destino}:\n"
                    f"Resultado: {resultado:.6f} {unidade_destino}"
                )

    return render(request, 'calculos/conversao.html', {'form': form, 'resultado': resultado, 'explicacao': explicacao})


def gerar_relatorio(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 750, "Relatório de Resultados Químicos")
    p.drawString(100, 700, "Exemplo de mistura ou diluição")
    p.showPage()
    p.save()
    return response

def sobre_teorias(request):
    return render(request, 'calculos/sobre_teorias.html')

