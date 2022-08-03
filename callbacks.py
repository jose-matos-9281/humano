from dash import  html,dcc
import plotly.express as px
from data_funcion import *
from data_clean import *
import layout as ly 

def render_content(tab):
    option = [
            {"label": "Medidas Principales", "value": 1},
            {"label": 'Metricas de Seguimiento',"value": 2},
            {"label": 'Metricas Hospitalarias', "value": 3},
        ]
    if tab == 'metricas':
        return [option,1,[ly.pagina_Series]]
    elif tab == 'SIR':
        option = [
                {"label": "S-I-R", "value": 4},
                {"label": 'Parametros SIR',"value": 5},
                {"label": 'Modelado', "value": 6},
            ]
        return [option,4,[ly.pagina_Series]
        ]
    elif tab == 'mapa':
        option =[]
        return [option,1,[
            html.H3('mapa'),
            dcc.Graph(id='graph-map')
        ]]
    elif tab == 'doc':
        option =[]
        return [option,1,[
            html.H3('Documentos'),
            dcc.Graph(id='graph-map')
        ]]

def display_choropleth(candidate):
    df = px.data.election()
    geojson = px.data.election_geojson()
    fig = px.choropleth_mapbox(df, geojson=geojson, color="winner",
                           locations="district", featureidkey="properties.district",
                           center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="carto-positron", zoom=9)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

def update_graph(
         datos, serie,
         provincia,inicio,
         fin, cum, mm =1,
         facet = False,
         func = px.line,
         titulo = " "):
    serie = [f'A_{i}' if f'A_{i}' in data.columns else i for i in serie] if cum == ['Acumulado'] else serie
    if facet:
        fig = func(grafico_M(datos,serie,inicio,fin,provincia,mm),facet_row='metrica')
    else:
        fig = func(grafico_M(datos,serie,inicio,fin,provincia,mm))
    fig.update_yaxes(matches=None)
    fig.update_layout(title= dict(
        text = titulo, y = 1, x=0.5, xanchor = 'center'
        ), legend = dict(
        orientation ='h',
        yanchor ='bottom',
        y = 1.0,
        xanchor = 'right',
        x =1
        ))
    return fig

def update_graph_H(
         datos, serie,
         inicio,fin,
         cum, mm =1,
         facet = False,
         func = px.line,
         titulo = ''):
    if facet:
        fig = func(grafico_H(datos,serie,inicio,fin,mm),facet_row='metrica')
    else:
        fig = func(grafico_H(datos,serie,inicio,fin,mm))

    fig.update_yaxes(matches=None)
    fig.update_layout(title= dict(
        text = titulo, y = 1, x=0.5, xanchor = 'center'
        ),legend = dict(
        orientation ='h',
        yanchor ='bottom',
        y = 0.98,
        xanchor = 'right',
        x =1
        ))
    return fig

def select_graph(provincia,inicio,fin, cum,par):
    
    graph = [
        update_graph(data,['Confirmados','Recuperados'],provincia,inicio,fin, cum,3,True, titulo = f'Cantidad de Confirmados y Recuperados  {cum[0] if cum != [] else "Por dia"} en {provincia}' ),
        update_graph(data,['Fallecidos'], provincia,inicio,fin, cum,1, titulo = f"Cantidad de Fallecidos {cum[0] if cum != [] else 'Por dia'} en {provincia}" ),
        update_graph(data,['Activos'], provincia,inicio,fin, cum,3, titulo = f"Cantidad de Activos por dia en {provincia}"),
        update_graph(data,['Muestras'], provincia,inicio,fin, cum, titulo = f'Cantidad de Muestras realizadas por Dia en {provincia}')
    ]
    if par == 2:
        
        graph = [
            update_graph(metricas,['positividad_4S','Letalidad'], provincia,inicio,fin, cum,3,True, titulo= f'Serie de tiempo Positividad 4 semanas y letalidad en {provincia}'),
            update_graph(data,['Confirmados', 'Muestras'], provincia,inicio,fin, [" "],3,True, titulo =f"Cantidad de Confirmados y cantidad de Muestras en {provincia}"),
            update_graph(metricas,['Incidencia_Ac','Prevalencia'], provincia,inicio,fin, cum,3,True,titulo = f"Incidencia Acumulada y Prevalencia por cada 100k hab en {provincia}" ),
            update_graph(metricas,['Duracion'], provincia,inicio,fin, cum,20,titulo = f"Duracion Promedio de la Enfermedad en {provincia}")
        ]

    elif par == 3:
        graph = [
            update_graph_H(metricas_H,['O_uci','O_c','O_ven'], inicio,fin, cum,facet=True,func=px.area, titulo = "Ocupacion Hospitalaria"),
            update_graph_H(metricas_H,['T_uci','T_c','T_ven','T'], inicio,fin, cum,facet=True,titulo = "Total de camas y ventiladores disponibles"),
            update_graph_H(metricas_H,['P_uci','P_c','P_ven','P_act'], inicio,fin, cum,facet=True, titulo = "Porcentaje de hospitalizacion"),
            update_graph_H(metricas_H,['p_c','p_uci','p_ven'], inicio,fin, cum,10, func = px.area, titulo = "Composicion de la hospotalizacion")
        ]
    elif par == 4:
        graph = [
            update_graph(sir,['S','I','R','F'],provincia, inicio,fin, cum,facet=True,func=px.line, titulo = "SIR"),
            update_graph(sir,['r','a','b'],provincia, inicio,fin, cum,facet=True,titulo = "Parametros"),
            update_graph(sir,['R0','Re','Pico'],provincia, inicio,fin, cum,facet=True, titulo = "Tasa de recuperacion y fallecimiento"),
            update_graph(sir,['Dias_R','Dias_F'],provincia, inicio,fin, cum,10, func = px.area, titulo = "Duracion promedio")
        ]

    return graph


def fecha_range(min, max):
    inicio = fecha[min]
    fin = fecha[max]
    return[inicio,fin]
def fecha_selector(min, max):
    inicio = indice[min]
    fin = indice[max]
    return[inicio,fin]