import pandas as pd
import numpy as np

def carregar_dados():
    df_setembro = pd.read_excel('_Dados do pedido(01-09-2026_30-09-2026).xlsx')
    df_outubro = pd.read_excel('_Dados do pedido(01-10-2026_31-10-2026).xlsx')
    return(pd.concat([df_setembro,df_outubro]).reset_index(drop= True))

def tratar_pedidos(df):
    df_copia = df.copy()
    df_copia = df_copia[df_copia['Horário do cancelamento'].isna()].reset_index(drop = True)
    df_copia['Tempo de preparo (minutos)'] = df_copia['Tempo de preparo (minutos)'].str.replace(',','.',regex = False)
    df_copia['Tempo de preparo (minutos)'] = pd.to_numeric(df_copia['Tempo de preparo (minutos)'],errors='coerce').replace(0,np.nan)
    df_copia['Data'] = df_copia['Data'].astype(str)
    df_copia['Data'] = pd.to_datetime(df_copia['Data'], format = '%Y%m%d')
    df_copia['Preparação atrasada?'] = df_copia['Preparação atrasada?'].map({'Sim':True,'Não':False})
    df_copia['nota'] = df_copia['Nível de avaliação do cliente'] / 100
    return(df_copia)

def criar_features(df):
    df_features = df.copy()
    df_features['mes'] = df_features['Data'].dt.month
    df_features['dia_semana'] = df_features['Data'].dt.dayofweek.map({0:'Segunda',1:'Terca',2:'Quarta',3:'Quinta',4:'Sexta',5:'Sabado',6:'Domingo'})
    df_features['faixa_preparo'] = pd.cut(df_features['Tempo de preparo (minutos)'],bins=[0,10,20,30,40,df_features['Tempo de preparo (minutos)'].max()],labels=['0-10','11-20','21-30','31-40','41+'])
    df_features['eh_nota_5'] = df_features['nota'] == 5
    df_features['marca'] = df_features['Nome do estabelecimento'].str.split(' - ').str[0].str.strip()
    return(df_features)

def resumir_por_faixa(df):
    df_resumido = df.groupby('faixa_preparo', observed = True).agg(pedidos = ('ID do pedido','count'), avaliacoes = ('nota','count'),nota_5 = ('eh_nota_5','sum'),nota_media = ('nota','mean'), taxa_atraso = ('Preparação atrasada?','mean')).reset_index()
    df_resumido['pct_5'] = df_resumido['nota_5'] / df_resumido['avaliacoes']
    return(df_resumido)

def faixa_pedidos_dia(df):
    df_faixa = df.groupby(['Data','Nome do estabelecimento']).agg(pedidos = ('ID do pedido','count'),avaliacoes = ('nota','count')).reset_index()
    df_faixa['faixa_pedidos'] = pd.cut(df_faixa['pedidos'],bins=[0,5,10,15,20,np.inf],labels=['1-5','6-10','11-15','16-20','21+'])
    df_faixa['teve_nota'] = df_faixa['avaliacoes'] > 0 
    df_faixa = df_faixa.groupby('faixa_pedidos',observed = True).agg(dias = ('pedidos','count'),com_nota = ('teve_nota','sum'),chance = ('teve_nota','mean')).reset_index()
    return(df_faixa) 

    