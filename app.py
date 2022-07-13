
from dash import Dash,Input, Output,html
import dash_bootstrap_components as dbc
import layout as ly
import callbacks as cb

stylesheets = [
    dbc.themes.SPACELAB
]

app = Dash(__name__,
        external_stylesheets=stylesheets
        )
server = app.server

app.layout = html.Div(ly.body)

@app.callback(            
            Output('Menus','options'),
            Output("Menus", "value"),
            Output('tabs-content', 'children'),
            Input('tabes', 'active_tab')
            )
def render_content(tab):
    return cb.render_content(tab)


@app.callback(
    Output("graph-map", "figure"), 
    Input("provincia", "value"))
def display_choropleth(candidate):
    return cb.display_choropleth(candidate)

@app.callback(
    Output('grafico_1', 'figure'),
    Output('grafico_2', 'figure'),
    Output('grafico_3', 'figure'),
    Output('grafico_4', 'figure'),
    Input('provincia','value'),
    Input('date-picker-range','start_date'),
    Input('date-picker-range','end_date'),
    Input('check-acum','value'),
    Input("Menus", "value"),
    suppress_callback_exceptions=True

)
def select_grafico( provincia,inicio,fin, cum,par):
    return cb.select_graph(provincia,inicio,fin, cum,par)

@app.callback(
    Output('date-picker-range', 'start_date'),
    Output('date-picker-range', 'end_date'),
    Input('my-range-slider', 'value'))
    
def update_fecha(value):
    return cb.fecha_range(value[0],value[1])

@app.callback(
    [Output('my-range-slider', 'value')],
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))
def update_rango(min,max):
    return [cb.fecha_selector(min,max)]

if __name__ == '__main__':
    app.run()