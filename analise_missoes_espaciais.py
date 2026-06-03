# =============================================================================
# ANÁLISE ESTATÍSTICA — MISSÕES ESPACIAIS (1957–2020)
# Dataset: Space Missions (Kaggle)
# =============================================================================

# -----------------------------------------------------------------------------
# IMPORT DAS BIBLIOTECAS NECESSÁRIAS
# -----------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# -----------------------------------------------------------------------------
# 0. CARREGAMENTO E LIMPEZA
# -----------------------------------------------------------------------------

df = pd.read_csv('data/Space_Corrected.csv')

# Renomear colunas
df.columns = [
    'idx1', 'idx2', 'empresa', 'localizacao',
    'data', 'detalhe', 'status_foguete', 'custo_milhoes', 'status_missao'
]

# Extrair ano
df['ano'] = pd.to_datetime(df['data'], format='%a %b %d, %Y %H:%M UTC', errors='coerce').dt.year

# Limpar custo (remover espaços, converter)
df['custo_milhoes'] = pd.to_numeric(df['custo_milhoes'], errors='coerce')

# Remover registros sem ano
df = df.dropna(subset=['ano'])
df['ano'] = df['ano'].astype(int)

print(f"Dataset carregado: {df.shape[0]} missões | {df.shape[1]} variáveis")
print(df[['empresa', 'ano', 'custo_milhoes', 'status_missao']].head())


# =============================================================================
# 1. TABELAS DE DISTRIBUIÇÃO DE FREQUÊNCIAS
# =============================================================================

print("\n" + "="*60)
print("TABELA 1 — VARIÁVEL DISCRETA: ANO DE LANÇAMENTO")
print("="*60)

# Frequência por ano (agrupado em décadas para melhor leitura)
df['decada'] = (df['ano'] // 10) * 10
freq_decada = df['decada'].value_counts().sort_index()

tabela_discreta = pd.DataFrame({
    'Década':         freq_decada.index.astype(str) + 's',
    'Freq. Absoluta': freq_decada.values,
    'Freq. Relativa (%)': (freq_decada.values / freq_decada.values.sum() * 100).round(2),
})
tabela_discreta['Freq. Acumulada'] = tabela_discreta['Freq. Absoluta'].cumsum()
tabela_discreta['Freq. Rel. Acum. (%)'] = tabela_discreta['Freq. Relativa (%)'].cumsum().round(2)
print(tabela_discreta.to_string(index=False))


print("\n" + "="*60)
print("TABELA 2 — VARIÁVEL CONTÍNUA: CUSTO DO LANÇAMENTO (US$ milhões)")
print("="*60)

custo = df['custo_milhoes'].dropna()

# Regra de Sturges
n = len(custo)
k = int(np.ceil(1 + 3.322 * np.log10(n)))
amplitude = custo.max() - custo.min()
h = amplitude / k

bins = np.arange(custo.min(), custo.max() + h, h)
labels = [f"{bins[i]:.0f} ⊢ {bins[i+1]:.0f}" for i in range(len(bins)-1)]

custo_cat = pd.cut(custo, bins=bins, labels=labels, include_lowest=True)
freq_custo = custo_cat.value_counts().sort_index()

tabela_continua = pd.DataFrame({
    'Classe (US$ mi)': freq_custo.index,
    'Freq. Absoluta':  freq_custo.values,
    'Freq. Relativa (%)': (freq_custo.values / freq_custo.values.sum() * 100).round(2),
})
tabela_continua['Freq. Acumulada'] = tabela_continua['Freq. Absoluta'].cumsum()
tabela_continua['Freq. Rel. Acum. (%)'] = tabela_continua['Freq. Relativa (%)'].cumsum().round(2)
print(tabela_continua.to_string(index=False))


# =============================================================================
# 2. GRÁFICOS ESTATÍSTICOS
# =============================================================================

plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.spines.top': False, 'axes.spines.right': False})

# --- GRÁFICO 1: Missões por Década ---
fig, ax = plt.subplots(figsize=(10, 6))
cores = ['#1a73e8' if d < 2000 else '#e84335' for d in freq_decada.index]
bars = ax.bar(tabela_discreta['Década'], tabela_discreta['Freq. Absoluta'], color=cores, edgecolor='white', linewidth=0.8)

for bar in bars:
    h_val = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h_val + 10, str(int(h_val)),
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_title('Número de Missões Espaciais por Década (1957–2020)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Década', fontsize=12)
ax.set_ylabel('Número de Missões', fontsize=12)
ax.legend(handles=[
    plt.Rectangle((0,0),1,1, color='#1a73e8', label='Guerra Fria / Corrida Espacial'),
    plt.Rectangle((0,0),1,1, color='#e84335', label='Nova Economia Espacial')
], fontsize=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.tight_layout()
plt.savefig('graficos/grafico1_missoes_por_decada.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nGráfico 1 salvo: graficos/grafico1_missoes_por_decada.png")


# --- GRÁFICO 2: Distribuição do Custo de Lançamento (Histograma + KDE) ---
fig, ax = plt.subplots(figsize=(10, 6))

custo_filtrado = custo[custo <= 500]  # Foco em 95% dos dados (remove outliers extremos)

ax.hist(custo_filtrado, bins=25, color='#1a73e8', edgecolor='white', alpha=0.8, density=True, label='Histograma')

kde = stats.gaussian_kde(custo_filtrado)
x_range = np.linspace(custo_filtrado.min(), custo_filtrado.max(), 300)
ax.plot(x_range, kde(x_range), color='#e84335', linewidth=2.5, label='Curva KDE')

ax.axvline(custo_filtrado.mean(), color='#fbbc04', linestyle='--', linewidth=1.8, label=f'Média: US${custo_filtrado.mean():.1f}M')
ax.axvline(custo_filtrado.median(), color='#34a853', linestyle='--', linewidth=1.8, label=f'Mediana: US${custo_filtrado.median():.1f}M')

ax.set_title('Distribuição do Custo de Lançamento (até US$ 500 milhões)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Custo (US$ milhões)', fontsize=12)
ax.set_ylabel('Densidade de Probabilidade', fontsize=12)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('graficos/grafico2_distribuicao_custo.png', dpi=150, bbox_inches='tight')
plt.close()
print("Gráfico 2 salvo: graficos/grafico2_distribuicao_custo.png")


# =============================================================================
# 3. ANÁLISES UNIVARIADAS — ESTATÍSTICA DESCRITIVA
# =============================================================================

def analise_univariada(serie, nome_variavel, unidade=''):
    print(f"\n{'='*60}")
    print(f"ANÁLISE UNIVARIADA: {nome_variavel.upper()}")
    print(f"{'='*60}")
    serie = serie.dropna()

    media    = serie.mean()
    mediana  = serie.median()
    moda_val = serie.mode()
    vmin     = serie.min()
    vmax     = serie.max()
    amplitude = vmax - vmin
    variancia = serie.var()
    dp        = serie.std()
    q1        = serie.quantile(0.25)
    q2        = serie.quantile(0.50)
    q3        = serie.quantile(0.75)
    iqr       = q3 - q1

    print(f"\n  Medidas de Tendência Central")
    print(f"    Média:    {media:.2f} {unidade}")
    print(f"    Mediana:  {mediana:.2f} {unidade}")
    print(f"    Moda:     {', '.join([f'{v:.2f}' for v in moda_val.values[:3]])} {unidade}")

    print(f"\n  Medidas de Dispersão")
    print(f"    Mínimo:       {vmin:.2f} {unidade}")
    print(f"    Máximo:       {vmax:.2f} {unidade}")
    print(f"    Amplitude:    {amplitude:.2f} {unidade}")
    print(f"    Variância:    {variancia:.2f}")
    print(f"    Desvio Padrão:{dp:.2f} {unidade}")

    print(f"\n  Medidas Separatrizes (Quartis)")
    print(f"    Q1 (25%): {q1:.2f} {unidade}")
    print(f"    Q2 (50%): {q2:.2f} {unidade}")
    print(f"    Q3 (75%): {q3:.2f} {unidade}")
    print(f"    IQR:      {iqr:.2f} {unidade}")

    return {
        'media': media, 'mediana': mediana, 'dp': dp,
        'q1': q1, 'q3': q3, 'vmin': vmin, 'vmax': vmax
    }


r1 = analise_univariada(df['ano'].astype(float), 'Ano de Lançamento', unidade='ano')
r2 = analise_univariada(df['custo_milhoes'], 'Custo de Lançamento', unidade='US$ mi')


# =============================================================================
# INTERPRETAÇÕES
# =============================================================================

print("""
================================================================================
INTERPRETAÇÃO DOS RESULTADOS
================================================================================

[ ANO DE LANÇAMENTO ]
A média dos lançamentos situa-se em torno de 1990, refletindo a grande
concentração de missões durante a Guerra Fria. O desvio padrão elevado
indica dispersão ao longo de mais de seis décadas. O Q3 (75%) ainda recai
nas décadas anteriores a 2000, evidenciando que a nova economia espacial
(pós-2000) representa uma parcela minoritária, mas crescente, do total.

[ CUSTO DE LANÇAMENTO ]
A diferença expressiva entre média e mediana indica forte assimetria positiva:
a maioria das missões tem custo relativamente baixo, mas missões de alto custo
(outliers) puxam a média para cima. O IQR concentra 50% dos lançamentos numa
faixa restrita, sugerindo que há um "custo padrão" no mercado, com poucos
lançamentos de altíssimo valor (missões governamentais de grande porte).
Essa assimetria é típica de mercados com agentes dominantes (NASA, ESA, Roscosmos)
coexistindo com operadores privados de menor escala.
================================================================================
""")

print("✅ Análise concluída com sucesso!")