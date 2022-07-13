
import datetime as dt
import pandas as pd
import data_clean as dc

def num(data,col):
    '''
    limpia la data numerica que tiene un caracter extra '-1
    '''
    for i in col:
        data[i]= data[i].str.replace("'","").astype("int32")
    return data

def data_pivot(data,serie):
    '''
    dado un dataframe crea la serie de tiempo por provincias, segun el parametro solicitado
    '''
    Frame = data.pivot_table(
        index = "fecha",
        columns = 'Provincia',
        values = serie
    )
    return Frame

def filtro_P (data,prov):
    return data[data.Provincia.isin(prov)]

def filtro_F (data,inicio = dt.datetime(2020,3,19), fin = dt.datetime(2022,7,3)): 
    return data[(data['fecha']>= inicio) & (data['fecha'] <= fin)]

def acumular(data,columna, func = 1, mm = 28):
    df = data_pivot(data,columna).copy()
    
    if func == 1:
        prefix = 'A'
        df = df.cumsum()
    elif  func == 2:
        prefix = 'D'
        df = df.diff()
    elif func == 3:
        prefix = 'MM'
        df = df.rolling(mm).mean()
    elif func == 4:
        df = df.rolling(mm).sum()
        
    df.insert(0,'fecha', df.index)
    df = pd.melt(df, id_vars='fecha',value_name = columna )
    df = df[['fecha','Provincia',columna]]
    return df.rename(columns = {columna: f'{prefix}_{columna}'})

def agregar(data,series, func = 1, mm= 28 ):
    for s in series:
        data = pd.merge_ordered(acumular(data,s,func,mm),data)
    return data

def grafico(data,metrica, 
        inicio = dt.datetime(2020,3,19),
        fin = dt.datetime(2022,7,3),
        prov = ['RD'], 
        mm =1 ):
    prueba = filtro_P(data,prov)
    prueba = filtro_F(prueba, inicio,fin)
    data_G = data_pivot(prueba,metrica).rolling(mm).mean()
    return data_G

def grafico_M(data,metricas,
              inicio = dt.datetime(2020,3,19),
              fin = dt.datetime(2022,7,3),
              prov = 'RD',
              mm =1 
             ):
    prueba = filtro_P(data,[prov]).drop('Provincia',axis = 1)
    prueba = filtro_F(prueba, inicio,fin)
    data_G = prueba.pivot_table(index = 'fecha',values = metricas).rolling(mm).mean()
    data_G.columns.name = 'metrica'
    return data_G

def grafico_H(data,metricas,
              inicio = dt.datetime(2020,3,19),
              fin = dt.datetime(2022,7,3),
              mm =1
             ):
    ser = [i.split("_")[-1] for i in metricas]
    ser = [dc.dic[i] if i in dc.dic else i for i in ser]
    leyend = dict(zip(metricas,ser))
    prueba = filtro_F(data, inicio,fin)
    data_G = prueba.pivot_table(index = 'fecha',values = metricas).rolling(mm).mean()
    data_G = data_G.rename(leyend,axis='columns')
    data_G.columns.name = 'metrica'
    return data_G


