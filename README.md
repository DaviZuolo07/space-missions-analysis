# Análise Estatística de Missões Espaciais (1957–2020)

> **Avaliação Global Solution — Estatística com Python**  
> Tema: Nova Economia Espacial
> Turma: 1CCPK

**Nome & RM Alunos:**
**Davi Queiroz Zuolo (571669);**
**Daniel Vilela Mana (571632),**
**Gustavo Zagato Botecchia (569420).**

---

## 🗂️ Estrutura do Repositório

```
space_missions/
│
├── data/
│   └── Space_Corrected.csv          # Base de dados original (Kaggle)
│
├── graficos/
│   ├── grafico1_missoes_por_decada.png   # Gerado automaticamente ao rodar o script
│   └── grafico2_distribuicao_custo.png   # Gerado automaticamente ao rodar o script
│
├── analise_missoes_espaciais.py      # Script principal com toda a análise
├── README.md                         # Este arquivo
└── relatorio_estatistico.pdf         # Relatório técnico final
```

---

## 📊 Base de Dados — Justificativa Técnica

| Critério | Avaliação |
|---|---|
| **Fonte** | Kaggle — dados públicos, rastreáveis e amplamente utilizados em projetos acadêmicos |
| **Origem real** | Compilado a partir de registros históricos da NASA, ESA, Roscosmos e outras agências |
| **Volume** | 4.324 registros (4.198 após limpeza), cobrindo 63 anos de história espacial |
| **Variáveis** | Empresa, localização, data, foguete, custo (US$ milhões), status da missão |
| **Aderência ao tema** | Alinhamento direto com o tema "Nova Economia Espacial" — permite analisar a transição do setor público para o privado (SpaceX, ULA, etc.) |
| **Potencial analítico** | Variáveis quantitativas discretas (ano) e contínuas (custo), além de variáveis categóricas para análises comparativas |

**Link da base:** https://www.kaggle.com/datasets/agirlcoding/all-space-missions-from-1957

---

## ⚙️ Como Executar

**Requisitos — instale as dependências:**
```bash
pip install pandas numpy matplotlib scipy
```

**Execute o script a partir da raiz do projeto:**
```bash
cd space_missions
python analise_missoes_espaciais.py
```

**O que acontece ao rodar:**
1. O terminal imprime todas as tabelas e análises formatadas
2. Dois arquivos `.png` são salvos automaticamente em `graficos/`
3. Nenhuma interação manual é necessária — tudo é gerado de uma vez

---

## 🔬 Como o Script Funciona — Passo a Passo

O arquivo `analise_missoes_espaciais.py` está dividido em **5 seções sequenciais**:

---

### Seção 0 — Carregamento e Limpeza

```python
df = pd.read_csv('data/Space_Corrected.csv')
```

- Lê o CSV da pasta `data/`
- Renomeia todas as colunas para nomes legíveis em português (`empresa`, `ano`, `custo_milhoes`, etc.)
- Extrai o **ano** da coluna `Datum`, que vem no formato `"Fri Aug 07, 2020 05:12 UTC"`, usando `pd.to_datetime`
- Converte a coluna de custo para `float` (era `object` por ter espaços e valores inválidos)
- Remove linhas sem ano válido (`dropna`)
- Imprime no terminal: shape do DataFrame e as 5 primeiras linhas

---

### Seção 1 — Tabelas de Distribuição de Frequências

**Tabela 1 — Variável Discreta: Ano de Lançamento**
- Agrupa os anos por **década** (`(ano // 10) * 10`)
- Calcula frequência absoluta, relativa (%), acumulada e relativa acumulada (%)
- Imprime a tabela completa no terminal

**Tabela 2 — Variável Contínua: Custo de Lançamento (US$ milhões)**
- Aplica a **Regra de Sturges** para definir o número ideal de classes: `k = 1 + 3.322 × log10(n)`
- Divide o intervalo de custo em `k` classes de amplitude igual usando `np.arange` + `pd.cut`
- Calcula as mesmas frequências da Tabela 1
- Imprime a tabela completa no terminal

---

### Seção 2 — Gráficos Estatísticos

**Gráfico 1 — Missões por Década** (`grafico1_missoes_por_decada.png`)
- Tipo: **gráfico de barras**
- Eixo X: décadas (1950s–2020s) | Eixo Y: número de missões
- Barras em **azul** para décadas da Guerra Fria e **vermelho** para a Nova Economia Espacial (pós-2000)
- Cada barra tem o valor numérico exibido no topo
- Legenda identificando os dois períodos históricos
- Salvo em `graficos/` via `plt.savefig`

**Gráfico 2 — Distribuição do Custo** (`grafico2_distribuicao_custo.png`)
- Tipo: **histograma com curva KDE** (Kernel Density Estimation)
- Filtra missões com custo até US$ 500M para focar em 95% dos dados e evitar distorção visual por outliers extremos
- Linha tracejada **amarela** marcando a média | Linha tracejada **verde** marcando a mediana
- Permite visualizar a assimetria positiva da distribuição
- Salvo em `graficos/` via `plt.savefig`

> ⚠️ Os gráficos **não abrem janela** — são salvos diretamente como arquivo. Isso é intencional para execução em qualquer ambiente.

---

### Seção 3 — Análises Univariadas

A função `analise_univariada(serie, nome, unidade)` é chamada **duas vezes**: para `ano` e para `custo_milhoes`.

Para cada variável, calcula e imprime no terminal:

| Categoria | Métricas |
|---|---|
| Tendência Central | Média, Mediana, Moda |
| Dispersão | Mínimo, Máximo, Amplitude, Variância, Desvio Padrão |
| Separatrizes | Q1 (25%), Q2 (50%), Q3 (75%), IQR |

---

### Seção 4 — Interpretação

Após os cálculos, o script imprime no terminal um bloco de interpretação crítica explicando:
- O que os dados do **ano de lançamento** revelam sobre a história espacial
- O que a **assimetria do custo** indica sobre a estrutura do mercado atual

---

## 💡 Principais Insights

- **70%+ das missões** ocorreram antes de 2000, durante a corrida espacial e Guerra Fria
- A **mediana do custo** (US$ 62M) é muito inferior à média (US$ 130M) — forte assimetria positiva
- A **moda de 2018** reflete o boom de lançamentos privados liderado pela SpaceX
- O mercado exibe estrutura **bimodal de custos**: missões econômicas (≤ US$ 86M, ~60%) e missões de alto valor (US$ 450M)

---

## 📚 Referências

- AGIRLCODING. *All Space Missions from 1957*. Kaggle, 2021. Disponível em: https://www.kaggle.com/datasets/agirlcoding/all-space-missions-from-1957
- IBGE. Portal Brasileiro de Dados Abertos. https://dados.gov.br
- NEXT SPACE ECONOMY. *The Space Economy at a Glance*. OCDE, 2022.
