# Avaliações em Delivery: volume de pedidos e tempo de preparo

**PT** | [EN](#english)

Análise de 40 mil pedidos de uma operação de dark kitchen multimarca (set–out/2026, dados anonimizados) para responder:

> Como o volume de pedidos e a performance de preparo influenciam a avaliação que as lojas recebem dos clientes?

Dashboard em **Streamlit** com filtros de mês, cidade e marca, mais um relatório completo com metodologia (`Relatorio_Trabalho_Final.pdf`).

![Gráficos do dashboard](docs/dashboard.png)

## Principais resultados

| Pergunta | Resultado |
|---|---|
| O volume muda a **chance** de ser avaliado? | Sim: de 27% (1–5 pedidos/dia) a 93% (21+). Em boa parte é efeito mecânico: só 9,6% dos pedidos são avaliados. |
| O volume muda a **qualidade** da nota? | Não: a proporção de notas 5 fica em 77–78% a partir de 6 pedidos/dia. |
| O tempo de preparo muda a nota? | Sim: nota média cai de 4,60 (até 10 min) para 3,90 (41+ min). A queda se acentua após 30 min. |
| Onde o preparo vira "atrasado"? | Entre 20 e 30 min (3% de atraso até 10 min; 53% entre 21–30; ~98% acima). |

**Limitações:** são associações, não causa; só 9,6% dos pedidos são avaliados (possível viés); a faixa 41+ min tem apenas 134 avaliações; a análise não separa efeito de loja, marca ou horário.

## Como rodar

```bash
git clone https://github.com/Silvairv/delivery-ratings-analysis.git
cd delivery-ratings-analysis
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura

| Arquivo | Função |
|---|---|
| `tratamento.py` | Carga, limpeza (cancelados, zeros, tipos) e criação de variáveis |
| `app.py` | Dashboard Streamlit |
| `_Dados do pedido(...).xlsx` | Bases de setembro e outubro (anonimizadas) |
| `Relatorio_Trabalho_Final.pdf` | Relatório com metodologia e conclusões |

## Tratamentos principais

- Remoção de pedidos cancelados (3.658) → 36.519 pedidos válidos.
- Nulos de avaliação mantidos como `NaN` (nulo = cliente não avaliou).
- Tempo de preparo `0` tratado como "não medido" (loja não marcou pronto) e convertido em `NaN`.
- Nota convertida da escala 100–500 para 1–5.

## Roadmap

- [ ] Comparar marcas e cidades
- [ ] Controlar efeito de loja e horário (regressão)
- [ ] Testes automatizados para `tratamento.py`
- [ ] Deploy público do dashboard (Streamlit Community Cloud)

## Dados

Os dados foram anonimizados (lojas e marcas codificadas, comentários removidos). Uso para fins educacionais e de portfólio.

---

## English

Analysis of 40k orders from a multi-brand delivery dark kitchen operation (Sep–Oct 2026, anonymized data) answering: *how do order volume and kitchen prep performance affect the ratings stores receive?*

Includes a **Streamlit** dashboard (filters by month, city, brand) and a full report in Portuguese (`Relatorio_Trabalho_Final.pdf`).

**Key findings**

- Order volume changes the *chance* of being rated (27% → 93% per store-day), largely mechanically since only 9.6% of orders are rated. It does **not** change rating *quality* (share of 5-star ratings stays ~77–78% from 6 orders/day).
- Prep time **does** affect rating quality: mean rating falls from 4.60 (≤10 min) to 3.90 (41+ min), with the drop accelerating after 30 min.
- Orders flip to "late" between 20 and 30 minutes.

**Caveats:** associations, not causal; only 9.6% of orders are rated; 41+ min bucket has few ratings (134); store/brand/time-of-day effects are not separated.

**Run locally**

```bash
pip install -r requirements.txt
streamlit run app.py
```

**Stack:** Python, pandas, NumPy, Matplotlib, Streamlit.
