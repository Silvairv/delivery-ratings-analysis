import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from tratamento import carregar_dados,tratar_pedidos,criar_features,resumir_por_faixa,faixa_pedidos_dia

# All user-facing text lives here, one block per language.
# To add a language or fix a sentence, edit only this dictionary.
TEXTOS = {
    'English': {
        'title': 'How do order volume and prep performance influence the ratings stores receive from customers?',
        'caption': 'September/October - 2026',
        'month': 'Month',
        'city': 'City',
        'brand': 'Brand',
        'no_orders': 'No orders match the selected filters',
        'total_orders': 'Total orders',
        'avg_rating': 'Average rating (rated orders)',
        'late_prep': 'Late preparation',

        'h1': 'The more orders in a day, the higher the chance the store gets rated?',
        'g1_title': 'Chance of getting at least one rating, by orders per day',
        'g1_x': 'Store orders per day',
        'g1_y': 'Chance of at least one rating (%)',
        'g1_caption': 'On days with {a} orders, the chance a store gets at least one rating is {pa:.0%}; on days with {b} orders, it rises to {pb:.0%}.',

        'h2': 'How is prep time distributed?',
        'g2_empty': 'No orders with measured prep time for the selected filters',
        'g2_median': 'Median: {m:.0f} min',
        'g2_title': 'Distribution of order prep time',
        'g2_x': 'Prep time (minutes)',
        'g2_y': 'Number of orders',
        'g2_caption': 'Median prep time is {m:.0f} minutes and {p:.0%} of orders are ready within 30 minutes. The chart omits the top 1% of orders above {l:.0f} minutes.',

        'h3': 'Does longer prep time mean a lower rating?',
        'g3_title': 'Average rating by prep time bucket',
        'g3_x': 'Prep time bucket (minutes)',
        'g3_y': 'Average rating',
        'g3_caption': 'Orders prepared in {a} minutes have an average rating of {ra:.2f}; for orders with {b} minutes, the average rating is {rb:.2f}.',

        'h4': 'At what prep time does an order start to be considered late?',
        'g4_title': 'Late preparation rate by prep time bucket',
        'g4_x': 'Prep time bucket (minutes)',
        'g4_y': 'Orders with late preparation (%)',
        'g4_caption': 'For orders prepared in {a} minutes, {ta:.0%} are late; for orders with {b} minutes, lateness reaches {tb:.0%}.',
    },
    'Português': {
        'title': 'Como o volume de pedidos e a performance de preparo influenciam a avaliação que as lojas recebem dos clientes?',
        'caption': 'Setembro/Outubro - 2026',
        'month': 'Mês',
        'city': 'Cidade',
        'brand': 'Marca',
        'no_orders': 'Nenhum pedido com os filtros selecionados',
        'total_orders': 'Total de pedidos',
        'avg_rating': 'Nota média dos pedidos avaliados',
        'late_prep': 'Preparação atrasada',

        'h1': 'Quanto mais pedidos no dia, maior a chance de a loja ser avaliada?',
        'g1_title': 'Chance de obter uma avaliação dentro de cada faixa de pedidos',
        'g1_x': 'Faixa de pedidos da loja no dia',
        'g1_y': 'Chance de ter ao menos uma avaliação (%)',
        'g1_caption': 'Em dias com {a} pedidos, a chance de a loja receber ao menos uma avaliação é de {pa:.0%}; em dias com {b} pedidos, passa a ser de {pb:.0%}.',

        'h2': 'Como se distribui o tempo de preparo dos pedidos?',
        'g2_empty': 'Nenhum pedido com tempo de preparo medido nos filtros selecionados',
        'g2_median': 'Mediana: {m:.0f} min',
        'g2_title': 'Distribuição do tempo de preparo dos pedidos',
        'g2_x': 'Tempo de preparo (minutos)',
        'g2_y': 'Número de pedidos',
        'g2_caption': 'A mediana do tempo de preparo é de {m:.0f} minutos e {p:.0%} dos pedidos saem em até 30 minutos. O gráfico não mostra o 1% de pedidos acima de {l:.0f} minutos.',

        'h3': 'Quanto maior o tempo de preparo, menor a nota?',
        'g3_title': 'Nota média por faixa de tempo de preparo',
        'g3_x': 'Faixa de Tempo de Preparo em Minutos',
        'g3_y': 'Nota média',
        'g3_caption': 'Pedidos preparados em {a} minutos têm nota média de {ra:.2f}; nos pedidos com {b} minutos, a nota média passa a ser {rb:.2f}.',

        'h4': 'Em que faixa de tempo a preparação passa a ser considerada atrasada?',
        'g4_title': 'Taxa de preparação atrasada por faixa de tempo de preparo',
        'g4_x': 'Faixa de Tempo de Preparo em Minutos',
        'g4_y': 'Pedidos com preparação atrasada (%)',
        'g4_caption': 'Em pedidos preparados em {a} minutos, {ta:.0%} têm preparação atrasada; nos pedidos com {b} minutos, o atraso chega a {tb:.0%}.',
    },
}

@st.cache_data
def carregar_tudo():
    resultado = criar_features(tratar_pedidos(carregar_dados()))
    return(resultado)

idioma = st.sidebar.radio('Language / Idioma', list(TEXTOS.keys()))
t = TEXTOS[idioma]

df = carregar_tudo()

opcoes_mes = sorted(df['mes'].unique())
opcoes_cidades = sorted(df['Cidade'].unique())
opcoes_marcas = sorted(df['marca'].unique())

meses = st.sidebar.multiselect(t['month'],opcoes_mes,default = opcoes_mes)
cidades = st.sidebar.multiselect(t['city'],opcoes_cidades,default = opcoes_cidades)
marcas = st.sidebar.multiselect(t['brand'],opcoes_marcas,default = opcoes_marcas)

df_filtrado = df[df['mes'].isin(meses)&df['Cidade'].isin(cidades)&df['marca'].isin(marcas)]

if df_filtrado.empty:
    st.warning(t['no_orders'])
    st.stop()

st.title(t['title'])

st.caption(t['caption'])

col1,col2,col3 = st.columns(3)

with col1:
    st.metric(t['total_orders'],f'{len(df_filtrado):,}')

with col2:
    st.metric(t['avg_rating'],f"{df_filtrado['nota'].mean():.2f}")

with col3:
    st.metric(t['late_prep'],f'{df_filtrado["Preparação atrasada?"].mean():.1%}')

st.subheader(t['h1'])

df_faixa = faixa_pedidos_dia(df_filtrado)
fig,ax = plt.subplots()

valores = ax.bar(df_faixa['faixa_pedidos'].astype(str),df_faixa['chance'] * 100)

ax.set_title(t['g1_title'])

ax.set_xlabel(t['g1_x'])

ax.set_ylabel(t['g1_y'])

ax.set_ylim(0,100)

ax.bar_label(valores, fmt = '%0.f%%')

st.pyplot(fig)

if len(df_faixa) > 1:
    primeira = df_faixa.iloc[0]
    ultima = df_faixa.iloc[-1]
    st.caption(t['g1_caption'].format(
        a = primeira['faixa_pedidos'], pa = primeira['chance'],
        b = ultima['faixa_pedidos'], pb = ultima['chance']))


st.subheader(t['h2'])

tempos = df_filtrado['Tempo de preparo (minutos)'].dropna()

if tempos.empty:
    st.info(t['g2_empty'])
else:
    limite = np.percentile(tempos,99)
    mediana = tempos.median()

    fig,ax = plt.subplots()

    ax.hist(tempos[tempos <= limite],bins = range(0,int(limite) + 3,2),edgecolor = 'white')

    ax.axvline(mediana,color = 'red',linestyle = '--',label = t['g2_median'].format(m = mediana))

    ax.set_title(t['g2_title'])

    ax.set_xlabel(t['g2_x'])

    ax.set_ylabel(t['g2_y'])

    ax.legend()

    st.pyplot(fig)

    st.caption(t['g2_caption'].format(m = mediana, p = (tempos <= 30).mean(), l = limite))


st.subheader(t['h3'])

df_resumido = resumir_por_faixa(df_filtrado)

fig, ax = plt.subplots()

valores_2 = ax.bar(df_resumido['faixa_preparo'].astype(str),df_resumido['nota_media'])

ax.set_title(t['g3_title'])

ax.set_ylim(3,5)

ax.bar_label(valores_2,fmt = '%.2f')

ax.set_xlabel(t['g3_x'])

ax.set_ylabel(t['g3_y'])

st.pyplot(fig)

if len(df_resumido) > 1:
    primeira = df_resumido.iloc[0]
    ultima = df_resumido.iloc[-1]
    st.caption(t['g3_caption'].format(
        a = primeira['faixa_preparo'], ra = primeira['nota_media'],
        b = ultima['faixa_preparo'], rb = ultima['nota_media']))

st.subheader(t['h4'])

fig,ax = plt.subplots()

ax.set_title(t['g4_title'])

valores_3 = ax.bar(df_resumido['faixa_preparo'].astype(str),df_resumido['taxa_atraso'] * 100)

ax.bar_label(valores_3, fmt = '%.0f%%')

ax.set_ylim(0,110)

ax.set_xlabel(t['g4_x'])

ax.set_ylabel(t['g4_y'])

st.pyplot(fig)

if len(df_resumido) > 1:
    primeira = df_resumido.iloc[0]
    ultima = df_resumido.iloc[-1]
    st.caption(t['g4_caption'].format(
        a = primeira['faixa_preparo'], ta = primeira['taxa_atraso'],
        b = ultima['faixa_preparo'], tb = ultima['taxa_atraso']))
