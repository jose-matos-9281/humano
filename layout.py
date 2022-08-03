
from dash import  html,dcc
import dash_bootstrap_components as dbc
from data_clean import *

header = html.Header(id="header",children=[
                html.H1(children='Análisis del Covid-19 en República Dominicana'),
            ]),
nav = dbc.CardHeader( id = 'nav', children=[
                    dbc.Tabs(id="tabes", active_tab='metricas', children=[
                        dbc.Tab(label='Metricas', tab_id='metricas'),
                        dbc.Tab(label='Modelo SIR', tab_id='SIR'),
                        dbc.Tab(label='Mapa', tab_id='mapa'),
                        dbc.Tab(label='Analisis', tab_id='doc')
                        
                    ])
            ])
SelectorFecha = dbc.Card([
                dbc.CardHeader('Rango de Fecha'),
                dbc.CardBody([
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date= f_inicio,
                            end_date= f_final,
                            min_date_allowed= f_inicio,
                            max_date_allowed= f_final,
                            end_date_placeholder_text='Select a date!'
                        )])],'S-fecha',class_name='margen t-50'
)
SelectorProvincia = dbc.Card([
                dbc.CardHeader('Provincia'),
                dbc.CardBody([
                    dcc.Dropdown( provincias, 'RD', id ='provincia'),
                    dcc.Checklist(['Acumulado'],['Acumulado'],id = 'check-acum')]
                )],class_name='margen'
)

lista = html.Div(
    [
        dbc.RadioItems(
            id="Menus",
            class_name='flex-container',
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary grande",
            labelCheckedClassName="active",
            options=[
                {"label": "Medidas Principales", "value": 1},
                {"label": 'Metricas de Seguimiento',"value": 2},
                {"label": 'Metricas Hospitalarias', "value": 3},
            ],
            value=1
        ),
    ],
    className="t-5"
)

menu = dbc.Card(id='lateral', children = [
    html.Div([SelectorFecha , SelectorProvincia], className='margen'),lista
                
    ] )

seccion = dbc.CardBody(id='contenido',children=[
                    html.Div([
                        dcc.RangeSlider(0,836, value=[0, 836],marks=mark, id='my-range-slider',allowCross=False)
                    ]),
                    html.Div(id='tabs-content',className="mt-3", style={'border': '2px'})
            ])

foot = html.Footer(id = 'foot', children=[
            html.H1("FOoor")
        ],
        style={
            'background-color': 'blue','width':'100%','heigth':'5rem'
        })


graph4 =[
        dcc.Graph(id = 'grafico_1',className='graph'),
        dcc.Graph(id = 'grafico_2',className='graph'),
        dcc.Graph(id = 'grafico_3',className='graph'),
        dcc.Graph(id = 'grafico_4',className='graph')
    ]

pagina_Series =  html.Div( children=graph4,id='Med_P', className='flex-container')

FiltroContent = dbc.Card([
                lista,
                dbc.CardBody([
                    dcc.Checklist(['Acumulado'],['Acumulado'],id = 'check-acum')
                ],'filtro-Content-body'
                )]
)
cards = dbc.Row(
    [
        dbc.Col([menu], lg=3,md=4),
        dbc.Col([dbc.Card([nav,seccion])], lg=9, md = 8),
    ]
)

body = dbc.Card(id= "body",children=[
    dbc.Row(dbc.Col(header,width={'size':11}), class_name='w-90',  justify='center',),
    dbc.Row(dbc.Col(dbc.Card( dbc.CardBody(cards)),width={'size':11}),justify='center')   
])