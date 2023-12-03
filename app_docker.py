from pgmpy.inference import VariableElimination
from dash.dependencies import Input, Output
from dotenv import load_dotenv
from dash import dcc  
from dash import html 
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import psycopg2
import pickle
import dash
import os

# Read model from PKL file 
#filename='model.pkl'
#file = open(filename, 'rb')
#model_success = pickle.load(file)
#file.close()

# Infering the posterior probability
infer = VariableElimination(model_success)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# path to env file
env_path=os.path.join("app.env")

# load env 
load_dotenv(dotenv_path=env_path)
# extract env variables
USER="postgres"
PASSWORD=os.getenv('PASSWORD')
HOST=os.getenv('HOST')
PORT=os.getenv('PORT')
DBNAME=os.getenv('DBNAME')

#connect to DB
engine = psycopg2.connect(
    dbname=DBNAME,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)
print(DBNAME)
print(USER)
print(PASSWORD)
print(HOST)
print(PORT)

cursor = engine.cursor()

content = [
    html.B("Inglés: "), html.Span(id='Ingles'), html.Br(),
    html.B("Matemáticas: "), html.Span(id='Matematicas'), html.Br(),
    html.B("Sociales: "), html.Span(id='Sociales')
    html.B("Ciencias Naturales: "), html.Span(id='Naturales')
    html.B("Lectura crítica: "), html.Span(id='Lectura')
]

app.layout = html.Div(
    [
    html.H1(children='Descubre el futuro de la educación del Atlántico', style={'text-align': 'center'}),
    html.Div(children='''
        ¿Te has Preguntado cómo Está Rindiendo el Atlántico en el Examen Saber 11? ¿Quisieras saber como te irá a ti en el examen? ¡Tenemos buenas noticias! Hemos creado 
        creado esta herramienta interactiva especialmente para ti, ciudadano del Atlántico.
    '''),
    html.H6("Estadísticas Descriptivas: Tu Departamento Bajo la Lupa")
    html.Div(children='''
        Con nuestro dashboard, ahora puedes explorar fácilmente las estadísticas de los resultados del examen Saber 11 en el Atlántico durante los últimos años.
    '''),
    html.Br(),
    dcc.Graph(id='comparativo')
    html.Div(["Selecciona área de ubicación del colegio: ",
              dcc.Dropdown(id='ubicacion', value="URBANO", 
                           options=["URBANO", "RURAL"])], style={'width': '48%', 'display': 'inline-block'}),
    html.Br(),
    dcc.Graph(id='colegios'),
    dcc.Graph(id='puntajes'),
    html.H6("Predecir el Futuro: ¿Cómo Te Irá en el Examen?")
    html.Div(children='''
        ¡Pero eso no es todo! Además de conocer las estadísticas pasadas, nuestro dashboard ofrece una función emocionante: ¡predecir los resultados del examen Saber 11! 
        Ingresa tus propios datos o los de alguien más y obtén una predicción de cómo podría ser el resultado del examen: '''),
    html.Br(),
    html.Div(["¿En qué área se encuentra tu colegio?: ",
              dcc.Dropdown(id='var1', value="URBANO", 
                           options=["URBANO", "RURAL"])]),
    html.Div(["¿Tu colegio es bilingue?: ",
              dcc.Dropdown(id='var2', value="S", 
                           options=["S","N","No se sabe"])]),
    html.Div(["¿Cuál es el género de tu colegio?: ",
              dcc.Dropdown(id='var3', value="MIXTO", 
                           options=["MIXTO","MASCULINO"])]),
    html.Div(["¿Cuál es la jornada de tu colegio?: ",
              dcc.Dropdown(id='var4', value="UNICA", 
                           options=["UNICA","COMPLETA","MANANA","TARDE","NOCHE","SABATINA"])]),     
    html.Div(["¿A qué edad presentarás el exámen?: ",
              dcc.Dropdown(id='var5', value=18, 
                           options=[ 16,  18,  20,  22])]),
    html.Div(["¿Con qué género te identificas?: ",
              dcc.Dropdown(id='var5', value="F", 
                           options=["F","M"])]),
    html.Div(["¿Cuántos cuartos tiene la casa en que resides?: ",
              dcc.Dropdown(id='var6', value="Tres", 
                           options=["Uno", "Dos", "Tres", "Cuatro", "Cinco", "Seis o mas"])]),
    html.Div(["¿Cuál es el nivel educativo de tu mamá?: ",
              dcc.Dropdown(id='var7', value=10, 
                           options=[ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12])]),
    html.Div(["¿Cuál es el nivel educativo de su papá?: ",
              dcc.Dropdown(id='var8', value=10, 
                           options=[ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12])]),    
    html.Div(["¿Cuál es tu estrato socieconómico?: ",
              dcc.Dropdown(id='var9', value="Estrato 3", 
                           options=[ "Estrato 1",  "Estrato 2",  "Estrato 3",  "Estrato 4",  "Estrato 5",  "Estrato 6", "Sin estrato"])]),                                                                                                
    html.Div(["¿Cuantas personas viven en tu casa?: ",
              dcc.Dropdown(id='var10', value="3 a 4", 
                           options=[ "1 a 2", "3 a 4", "5 a 6", "7 a 8", "9 o mas"])]),  
    html.Div(["¿Tu familia tiene computador?: ",
              dcc.Dropdown(id='var11', value="Si", 
                           options=[ "Si", "No"])]),  
    html.Div(["¿Tu casa tiene internet?: ",
              dcc.Dropdown(id='var12', value=15, 
                           options=[ "Si", "No"])]),  
    html.Br(),
    html.H6(children='''El estimado de tus puntajes en las diferentes áreas que evalua la Prueba Saber 11° es:'''), 
    html.Div(children=content),
    ]
)


@app.callback(
    Output(component_id='colegios', component_property='figure'),
    Output(component_id='puntajes', component_property='figure'),
    Input(component_id='ubicacion', component_property='value')
)

def update_graphs(area):

    # Consulta sobre los puntajes
    cursor = engine.cursor()
    query_puntajes = """
    SELECT 
    ano,
    AVG(punt_ingles) AS promedio_punt_ingles,
    AVG(punt_matematicas) AS promedio_punt_matematicas,
    AVG(punt_sociales_ciudadanas) AS promedio_punt_sociales_ciudadanas,
    AVG(punt_c_naturales) AS promedio_punt_c_naturales,
    AVG(punt_lectura_critica) AS promedio_punt_lectura_critica
    FROM 
    saberpro_tabla
    WHERE 
    cole_area_ubicacion = {}
    GROUP BY ano;""".format(area)
    cursor.execute(query_puntajes)
    result_puntajes = cursor.fetchall()

    # Crear la figura del gráfico de exito
    fig_puntajes = go.Figure()

    fig_puntajes.add_trace(go.Bar(
        x=[result_exito[0][0]],
        y=[result_exito[0][1]],
        name=result_exito[0][0],
        text=['{:.2f}'.format(result_exito[0][1])],
        textposition='auto',
        marker=dict(color='#660000')
    ))

    fig_puntajes.update_layout(barmode='group', title="Promedio de puntajes por año según el área de ubicación del colegio")
    
    #Consultas sobre caracteristicas colegios
    query_area = """
    SELECT 
    cole_area_ubicacion,
    COUNT(*) AS conteo_area_ubicacion
    FROM 
    saberpro_tabla
    GROUP BY 
    cole_area_ubicacion;"""
    cursor.execute(query_area)
    result_area = cursor.fetchall()

    query_bilingue = """
    SELECT 
    cole_bilingue,
    COUNT(*) AS conteo_bilingue
    FROM 
    tu_tabla
    GROUP BY 
    cole_bilingue;;"""
    cursor.execute(query_bilingue)
    result_bilingue = cursor.fetchall()

    query_genero = """
    SELECT
    cole_genero,
    COUNT(*) AS conteo_genero
    FROM
    tu_tabla
    GROUP BY
    cole_genero;"""
    cursor.execute(query_genero)
    result_genero = cursor.fetchall()

    query_jornada = """
    SELECT
    cole_jornada,
    COUNT(*) AS conteo_jornada,
    FROM
    tu_tabla,
    GROUP BY,
    cole_jornada;""" 
    cursor.execute(query_jornada)
    result_jornada = cursor.fetchall()   

    # Crear la figura del gráfico 
    fig_colegios = go.Figure()

    # Agregar las barras para primer semestre
    fig_colegios.add_trace(go.Bar(
        x=["Promedio 1er Semestre"],
        y=[first],
        name='1er Semestre',
        text=['{:.2f}'.format(first)],
        textposition='auto',
        marker=dict(color='#003399')
    ))

    fig_colegios.add_trace(go.Bar(
        x=["Promedio 1er Semestre (General)"],
        y=[first_general],
        name='1er Semestre (General)',
        text=['{:.2f}'.format(first_general)],
        textposition='auto',
        marker=dict(color='#0099FF')
    ))

    fig_colegios.update_layout(barmode='group', title="Características de los colegios del atlántico")

    return fig_puntajes, fig_colegios

@app.callback(
    Output(component_id='Ingles', component_property='children'),
    Output(component_id='Matematicas', component_property='children'),
    Output(component_id='Sociales', component_property='children'),
    Output(component_id='Naturales', component_property='children'),
    Output(component_id='Lectura', component_property='children'),
    [
        Input(component_id='var1', component_property='value'),
        Input(component_id='var2', component_property='value'),
        Input(component_id='var3', component_property='value'),
        Input(component_id='var4', component_property='value'),
        Input(component_id='var5', component_property='value'),
        Input(component_id='var6', component_property='value'),
        Input(component_id='var7', component_property='value'),
        Input(component_id='var8', component_property='value'),
        Input(component_id='var9', component_property='value'),
        Input(component_id='var10', component_property='value'),
        Input(component_id='var11', component_property='value'),
        Input(component_id='var12', component_property='value')
    ]
)
        
def update_prediction(val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12):
    # Predicción del estado estudiantil
    values = [val1, val2, val3, val4, val5, val6, val7, val8, val9, val10, val11, val12]
    labels = ["cole_area_ubicacion","cole_bilingue","cole_genero","cole_jornada","edad_presentacion",
                "estu_genero","fami_cuartoshogar","fami_educacionmadre_cod","fami_educacionpadre_cod",
                "fami_estratovivienda","fami_personashogar","fami_tienecomputador","fami_tieneinternet"]
    evidence = {}
    for i in range(len(values)):
        if values[i] != '':
            evidence[labels[i]]=int(values[i])
    result = infer.query(variables=['target'], evidence=evidence)
    list_result = list(result.values)

    return round(list_result[0],2), round(list_result[1],2), round(list_result[2],2), round(list_result[3],2), round(list_result[4],2)

if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8020)