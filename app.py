import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from tratamento import carregar_dados,tratar_pedidos,criar_features,resumir_por_faixa,faixa_pedidos_dia

@st.cache_data

def carregar_tudo():
    resultado = criar_features(tratar_pedidos(carregar_dados()))
    return(resultado)

df = carregar_tudo()

opcoes_mes = sorted(df['mes'].unique())
opcoes_cidades = sorted(df['Cidade'].unique())
opcoes_marcas = sorted(df['marca'].unique())

meses = st.sidebar.multiselect('Mês',opcoes_mes,default = opcoes_mes)
cidades = st.sidebar.multiselect('Cidade',opcoes_cidades,default = opcoes_cidades)
marcas = st.sidebar.multiselect('Marca',opcoes_marcas,default = opcoes_marcas)

df_filtrado = df[df['mes'].isin(meses)&df['Cidade'].isin(cidades)&df['marca'].isin(marcas)]

if df_filtrado.empty:
    st.warning('Nenhum pedido com os filtros selecionados')
    st.stop()

st.title('Como o volume de pedidos e a performance de preparo influenciam a avaliação que as lojas recebem dos clientes?')

st.caption('Setembro/Outubro - 2026')

col1,col2,col3 = st.columns(3)

with col1:
    st.metric("Total de pedidos",f'{len(df_filtrado):,}')

with col2:
    st.metric("Nota média dos pedidos avaliados",f"{df_filtrado['nota'].mean():.2f}")

with col3:
    st.metric("Preparação atrasada",f'{df_filtrado["Preparação atrasada?"].mean():.1%}')

st.subheader('Quanto mais pedidos no dia, maior a chance de a loja ser avaliada?')

df_faixa = faixa_pedidos_dia(df_filtrado)
fig,ax = plt.subplots()

valores = ax.bar(df_faixa['faixa_pedidos'].astype(str),df_faixa['chance'] * 100)

ax.set_title('Chance de obter uma avaliação dentro de cada faixa de pedidos')

ax.set_xlabel('Faixa de pedidos da loja no dia')

ax.set_ylabel('Chance de ter ao menos uma avaliação (%)')

ax.set_ylim(0,100)

ax.bar_label(valores, fmt = '%0.f%%')

st.pyplot(fig)

if len(df_faixa) > 1:
    primeira = df_faixa.iloc[0]
    ultima = df_faixa.iloc[-1]
    st.caption(
        f"Em dias com {primeira['faixa_pedidos']} pedidos, a chance de a loja receber "
        f"ao menos uma avaliação é de {primeira['chance']:.0%}; em dias com "
        f"{ultima['faixa_pedidos']} pedidos, passa a ser de {ultima['chance']:.0%}."
    )


st.subheader('Como se distribui o tempo de preparo dos pedidos?')

tempos = df_filtrado['Tempo de preparo (minutos)'].dropna()

if tempos.empty:
    st.info('Nenhum pedido com tempo de preparo medido nos filtros selecionados')
else:
    limite = np.percentile(tempos,99)
    mediana = tempos.median()

    fig,ax = plt.subplots()

    ax.hist(tempos[tempos <= limite],bins = range(0,int(limite) + 3,2),edgecolor = 'white')

    ax.axvline(mediana,color = 'red',linestyle = '--',label = f'Mediana: {mediana:.0f} min')

    ax.set_title('Distribuição do tempo de preparo dos pedidos')

    ax.set_xlabel('Tempo de preparo (minutos)')

    ax.set_ylabel('Número de pedidos')

    ax.legend()

    st.pyplot(fig)

    st.caption(
        f"A mediana do tempo de preparo é de {mediana:.0f} minutos e {(tempos <= 30).mean():.0%} "
        f"dos pedidos saem em até 30 minutos. O gráfico não mostra o 1% de pedidos acima de {limite:.0f} minutos."
    )


st.subheader('Quanto maior o tempo de preparo, menor a nota?')

df_resumido = resumir_por_faixa(df_filtrado)

fig, ax = plt.subplots()

valores_2 = ax.bar(df_resumido['faixa_preparo'].astype(str),df_resumido['nota_media'])

ax.set_title('Nota média por faixa de tempo de preparo')

ax.set_ylim(3,5)

ax.bar_label(valores_2,fmt = '%.2f')

ax.set_xlabel('Faixa de Tempo de Preparo em Minutos')

ax.set_ylabel('Nota média')

st.pyplot(fig)

if len(df_resumido) > 1:
    primeira = df_resumido.iloc[0]
    ultima = df_resumido.iloc[-1]
    st.caption(
        f"Pedidos preparados em {primeira['faixa_preparo']} minutos têm nota média de "
        f"{primeira['nota_media']:.2f}; nos pedidos com {ultima['faixa_preparo']} minutos, "
        f"a nota média passa a ser {ultima['nota_media']:.2f}."
    )

st.subheader('Em que faixa de tempo a preparação passa a ser considerada atrasada?')

fig,ax = plt.subplots()

ax.set_title('Taxa de preparação atrasada por faixa de tempo de preparo')

valores_3 = ax.bar(df_resumido['faixa_preparo'].astype(str),df_resumido['taxa_atraso'] * 100)

ax.bar_label(valores_3, fmt = '%.0f%%')

ax.set_ylim(0,110)

ax.set_xlabel('Faixa de Tempo de Preparo em Minutos')

ax.set_ylabel('Pedidos com preparação atrasada (%)')

st.pyplot(fig)

if len(df_resumido) > 1:
    primeira = df_resumido.iloc[0]
    ultima = df_resumido.iloc[-1]
    st.caption(
        f"Em pedidos preparados em {primeira['faixa_preparo']} minutos, "
        f"{primeira['taxa_atraso']:.0%} têm preparação atrasada; "
        f"nos pedidos com {ultima['faixa_preparo']} minutos, o atraso chega a {ultima['taxa_atraso']:.0%}."
    )