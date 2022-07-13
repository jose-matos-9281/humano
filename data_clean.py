import pandas as pd
import numpy as np
from data_funcion import *

f_inicio = dt.datetime(2020,3,19)
f_final = dt.datetime(2022,7,3)

hosp = pd.read_csv('data/hospitalizacion.csv')
data = pd.read_csv('data/data.csv')
data['fecha']= pd.to_datetime(data['fecha'])

fecha= pd.Series(data.sort_values('fecha').fecha.unique())
indice = pd.Series(fecha.index,fecha)
mark = {
    13: 'abr-2020',
    104: 'jul-2020',
    196: 'oct-2020',    
    288: 'ene-2021',
    378: 'abr-2021',
    469: 'jul-2021',
    561: 'oct-2021',
    653: 'ene-2022',
    743: 'abr-2022',
    834: 'jul-2022'
}

data_C = num(data,['Confirmados', 'Fallecidos', 'Muestras','Recuperados'])
hosp['fecha']= pd.to_datetime(hosp['fecha'])
hosp.columns= ['fecha', 'Hosp', 'O_camas', 'O_UCI', 'O_ventiladores',
       'T_camas', 'T_UCI', 'T_ventiladores', 'Conf',
       'Recp', 'Fall',
       'A_Conf', 'A_Recp',
       'A_Fall']

Series_MP =['Confirmados', 'Fallecidos', 'Muestras','Recuperados']
Series_MPA =['A_Confirmados', 'A_Fallecidos', 'A_Muestras','A_Recuperados']
Series_SIR = ['S','I','R']
Series_SIR_M = ['R0','Re','Dias_R','Dias_F']
Series_MS = ['positividad_4S','positividad_2S','positividad_5D','Letalidad']

serie = lambda data: data.columns.drop(['fecha','Provincia'])
provincias = ['Azua', 'Baoruco', 'Barahona', 'Dajabón', 'Distrito Nacional', 'Duarte',
       'El Seibo', 'Elías Piña', 'Espaillat', 'Hato Mayor', 'Hermanas Mirabal',
       'Independencia', 'La Altagracia', 'La Romana', 'La Vega',
       'María Trinidad Sánchez', 'Monseñor Nouel', 'Monte Cristi',
       'Monte Plata', 'Pedernales', 'Peravia', 'Puerto Plata', 'RD', 'Samaná',
       'San Cristóbal', 'San José de Ocoa', 'San Juan', 'San Pedro de Macorís',
       'Santiago', 'Santiago Rodríguez', 'Santo Domingo', 'Sánchez Ramírez',
       'Valverde']

data = agregar(data_C,["Confirmados","Fallecidos","Muestras","Recuperados"])
data = data.assign(Activos = data.A_Confirmados - data.A_Fallecidos - data.A_Recuperados)

sir = data[['fecha', 'Provincia']]
sir = sir.assign( 
    N = data.Poblacion,
    S = data.Poblacion - data.A_Confirmados,
    I = data.Activos, 
    R = data.A_Recuperados,
    F = data.A_Fallecidos,
    D_F = data.Fallecidos,
    D_R = data.Recuperados
)

sir = agregar(sir, ['S','I'],2)
sir = sir.assign(
    r = -sir.D_S/(sir.S*sir.I), 
    a = sir.D_R/sir.I, 
    b = sir.D_F/sir.I
)

aux = (sir.a+sir.b)/sir.r
sir = sir.assign(
    R0 = sir.r*sir.N/(sir.a +sir.b),
    Dias_R = 1/sir.a,
    Dias_F = 1/sir.b,
    Re = sir.r*sir.S/(sir.a +sir.b),
    Pico = aux*np.log(aux/sir.S)-aux +sir.I + sir.S
).fillna(0)

metricas = data[['fecha', 'Provincia','Activos','Confirmados','Fallecidos','Recuperados']]
Posi = lambda dias : (agregar(data,['Confirmados'],3,dias)['MM_Confirmados']/agregar(data,["Muestras"],3, dias)['MM_Muestras']).fillna(0)

metricas = metricas.assign( 
    positividad_4S = Posi(28),
    positividad_2S = Posi(14),
    positividad_3D = Posi(3),
    mortalidad_G   = data.A_Fallecidos/data.Poblacion,
    Letalidad      = data.A_Fallecidos/data.A_Confirmados,
    Prevalencia    = (data.Activos/data.Poblacion)*100000,
    Incidencia_Ac  = (data.A_Confirmados/data.Poblacion)*100000
).fillna(0)

metricas = metricas.assign(
    D_Incidencia_Ac =agregar(metricas,['Incidencia_Ac'],2)['D_Incidencia_Ac']
    ).fillna(0)
metricas = metricas.assign(
    Duracion = metricas.Prevalencia/metricas.D_Incidencia_Ac
    ).fillna(0)

metricas_H = hosp[['fecha']]
hosp = hosp.assign(
    activos = hosp.A_Conf-hosp.A_Recp-hosp.A_Fall
)
metricas_H = metricas_H.assign(
    Hosp = hosp.Hosp,
    Act = hosp.activos,
    O_c = hosp.O_camas,
    O_uci = hosp.O_UCI,
    O_ven = hosp.O_ventiladores,
    T_c = hosp.T_camas,
    T_uci = hosp.T_UCI,
    T_ven = hosp.T_ventiladores,
    P_c = hosp.O_camas/hosp.T_camas,
    P_uci = hosp.O_UCI/hosp.T_UCI,
    P_ven = hosp.O_ventiladores/hosp.T_ventiladores,
    P_act = hosp.Hosp/(hosp.activos-hosp.Conf+hosp.Recp+hosp.Fall),
    T = hosp.T_camas+hosp.T_UCI+hosp.T_ventiladores,
    p_c = hosp.O_camas/hosp.Hosp,
    p_uci = hosp.O_UCI/hosp.Hosp,
    p_ven = hosp.O_ventiladores/hosp.Hosp,
      
)

dic = {
    'uci':"UCI",
    'c':'Camas',
    'ven':"Ventiladores",
    'T':'Total',
    'act':'Activos'
}