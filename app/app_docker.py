from pgmpy.inference import VariableElimination
from dash.dependencies import Input, Output
#from dotenv import load_dotenv
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
filename='model.pkl'
file = open(filename, 'rb')
model_success = pickle.load(file)
file.close()

# Infering the posterior probability
infer = VariableElimination(model_success)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# path to env file
env_path=os.path.join("app.env")

# load env 
#load_dotenv(dotenv_path=env_path)
# extract env variables
#USER=os.getenv('USER')
#PASSWORD=os.getenv('PASSWORD')
#HOST=os.getenv('HOST')
#PORT=os.getenv('PORT')
#DBNAME=os.getenv('DBNAME')

USER="postgres"
PASSWORD="saberpro"
HOST="saberprodatabase.cc8qstu92fve.us-east-1.rds.amazonaws.com"
PORT="5432"
DBNAME="saberpro"

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

app.layout = html.Div(
    [
    html.H1(children='Descubre el futuro de la educación del Atlántico', style={'text-align': 'center'}),
    html.Div(children='''
        ¿Te has preguntado cómo está el desempeño del Atlántico en el Examen Saber 11? ¿Quisieras saber como te irá a ti en el examen? ¡Tenemos buenas noticias! Hemos creado 
        creado esta herramienta interactiva especialmente para ti, ciudadano del Atlántico.
    '''),
    html.H6("Estadísticas Descriptivas: Tu Departamento Bajo la Lupa"),
    html.Div(children='''
        Con nuestro dashboard, ahora puedes explorar fácilmente las estadísticas de los resultados del examen Saber 11 en el Atlántico durante los últimos años.
    '''),
    html.Br(),
    html.Div(
        html.Iframe(
            src="https://www.datos.gov.co/dataset/PUNTAJE-ICFES-POR-DEPARTAMENTOS/x9vi-iv8c/embed?width=1200&height=500",
            style={"width": "1200px", "height": "500px", "border": "0"}
            ),
        style={"display": "flex", "justifyContent": "center"},
        ),
    html.Br(),
    dcc.Graph(id='colegios'),
    html.Div(["Selecciona área de ubicación del colegio: ",
              dcc.Dropdown(id='ubicacion', value="URBANO", 
                           options=["URBANO", "RURAL"])], style={'width': '48%', 'display': 'inline-block'}),
    dcc.Graph(id='puntajes'),
    html.H6("Predecir el Futuro: ¿Cómo Te Irá en el Examen?"),
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
    #html.Div(["¿Cuál es el género de tu colegio?: ",  dcc.Dropdown(id='var3', value="MIXTO",options=["MIXTO","MASCULINO"])]),
    #html.Div(["¿Cuál es la jornada de tu colegio?: ", dcc.Dropdown(id='var4', value="UNICA", options=["UNICA","COMPLETA","MANANA","TARDE","NOCHE","SABATINA"])]),     
    html.Div(["¿A qué edad presentarás el exámen?: ",
              dcc.Dropdown(id='var5', value=18, 
                           options=[ 16,  18,  20,  22])]),
    html.Div(["¿Con qué género te identificas?: ",
              dcc.Dropdown(id='var6', value="F", 
                           options=["F","M"])]),
    #html.Div(["¿Cuántos cuartos tiene la casa en que resides?: ", dcc.Dropdown(id='var7', value="Tres", options=["Uno", "Dos", "Tres", "Cuatro", "Cinco", "Seis o mas"])]),
    html.Div(["¿Cuál es el nivel educativo de tu mamá?: ",
              dcc.Dropdown(id='var8', value=10, 
                           options=[ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12])]),
    html.Div(["¿Cuál es el nivel educativo de su papá?: ",
              dcc.Dropdown(id='var9', value=10, 
                           options=[ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12])]),    
    html.Div(["¿Cuál es tu estrato socieconómico?: ",
              dcc.Dropdown(id='var10', value="Estrato 3", 
                           options=[ "Estrato 1",  "Estrato 2",  "Estrato 3",  "Estrato 4",  "Estrato 5",  "Estrato 6", "Sin estrato"])]),                                                                                                
    html.Div(["¿Cuantas personas viven en tu casa?: ",
              dcc.Dropdown(id='var11', value="3 a 4", 
                           options=[ "1 a 2", "3 a 4", "5 a 6", "7 a 8", "9 o mas"])]),  
    html.Div(["¿Tu familia tiene computador?: ",
              dcc.Dropdown(id='var12', value="Si", 
                           options=[ "Si", "No"])]),  
    html.Div(["¿Tu casa tiene internet?: ",
              dcc.Dropdown(id='var13', value="Si", 
                           options=[ "Si", "No"])]),  
    html.Br(),
    html.H6(children='''El estimado de tu puntaje global en la Prueba Saber 11° es:'''), 
    html.Span(id='puntaje'),
    ]
)


@app.callback(
    Output(component_id='puntajes', component_property='figure'),
    Output(component_id='colegios', component_property='figure'),
    Input(component_id='ubicacion', component_property='value')
)

def update_graphs(ubicacion):

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
    cole_area_ubicacion = '{}'
    GROUP BY ano;""".format(ubicacion)
    cursor.execute(query_puntajes)
    result_puntajes = cursor.fetchall()

    # Crear la figura del gráfico de exito
    fig_puntajes = go.Figure()

    result_puntajes_float = []

    for i in range(len(result_puntajes)):
        result_puntajes_float.append([])
        for j in range(len(result_puntajes[i])):
            result_puntajes_float[i].append(float(result_puntajes[i][j]))

    df_convertido = pd.DataFrame(result_puntajes_float, columns=['Año', 'Promedio Ingles', 'Promedio Matematicas', 
                                                            'Promedio Sociales Ciudadanas', 'Promedio Ciencias Naturales', 
                                                            'Promedio Lectura Critica'])

    # Convertir los datos para el uso con Plotly
    data = []

    # Añadir cada asignatura como una serie separada
    for asignatura in df_convertido.columns[1:]:
        data.append(
            go.Bar(
                x=df_convertido['Año'],
                y=df_convertido[asignatura],
                name=asignatura
            )
        )

    # Configuración del layout del gráfico
    layout = go.Layout(
        title='Promedios de Puntajes por Año',
        xaxis=dict(title='Año'),
        yaxis=dict(title='Promedio de Puntajes para los último años'),
        barmode='group'
    )

    # Crear la figura con los datos y el layout
    fig_puntajes = go.Figure(data=data, layout=layout)
    
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
        saberpro_tabla
        GROUP BY 
        cole_bilingue;;"""
    cursor.execute(query_bilingue)
    result_bilingue = cursor.fetchall()

    query_genero = """
        SELECT
        cole_genero,
        COUNT(*) AS conteo_genero
        FROM
        saberpro_tabla
        GROUP BY
        cole_genero;"""
    cursor.execute(query_genero)
    result_genero = cursor.fetchall()

    query_jornada = """
        SELECT
        cole_jornada,
        COUNT(*) AS conteo_jornada
        FROM
        saberpro_tabla
        GROUP BY
        cole_jornada;""" 
    cursor.execute(query_jornada)
    result_jornada = cursor.fetchall()

    # Función para crear un gráfico de barras con Plotly
    def create_bar_plot(data, title):
        labels, values = zip(*data)
        bar_plot = go.Bar(x=labels, y=values, name=title)
        return bar_plot

    # Crear los gráficos de barras
    bar1 = create_bar_plot(result_area, 'Área de Ubicación')
    bar2 = create_bar_plot(result_bilingue, 'Bilingüe')
    bar3 = create_bar_plot(result_genero, 'Género')
    bar4 = create_bar_plot(result_jornada, 'Jornada')

    # Crear una figura para mostrar los gráficos
    fig_colegios = go.Figure(data=[bar1, bar2, bar3, bar4])

    # Actualizar el layout de la figura
    fig_colegios.update_layout(
        barmode='group',
        title='Características de los colegios del Atlántico',
        xaxis=dict(title='Categorías'),
        yaxis=dict(title='Valores')
    )

    return fig_puntajes, fig_colegios

@app.callback(
    Output(component_id='puntaje', component_property='children'),
    [
        Input(component_id='var1', component_property='value'),
        Input(component_id='var2', component_property='value'),
        #Input(component_id='var3', component_property='value'),
        #Input(component_id='var4', component_property='value'),
        Input(component_id='var5', component_property='value'),
        Input(component_id='var6', component_property='value'),
        #Input(component_id='var7', component_property='value'),
        Input(component_id='var8', component_property='value'),
        Input(component_id='var9', component_property='value'),
        Input(component_id='var10', component_property='value'),
        Input(component_id='var11', component_property='value'),
        Input(component_id='var12', component_property='value'),
        Input(component_id='var13', component_property='value')
    ]
)
        
def update_prediction(var1, var2, var5, var6, var8, var9, var10, var11, var12, var13):
    # Predicción del estado estudiantil
    values = [var1, var2, var5, var6, var8, var9, var10, var11, var12, var13]
    labels = ["cole_area_ubicacion","cole_bilingue","edad_presentacion",
                "estu_genero","fami_educacionmadre_cod","fami_educacionpadre_cod",
                "fami_estratovivienda","fami_personashogar","fami_tienecomputador","fami_tieneinternet"]
    evidence = {}
    for i in range(len(values)):
        if values[i] != '':
            evidence[labels[i]]=values[i]
    result = infer.query(variables=['punt_total'], evidence=evidence)
    list_result = list(result.values)

    prediction=0

    max_val = list_result.index(max(result.values))
    if max_val == 0:
        prediction = 160
    elif max_val == 1:
        prediction = 180
    elif max_val == 2:
        prediction = 200
    elif max_val == 3:
        prediction = 220
    elif max_val == 4:
        prediction = 240
    elif max_val == 5:
        prediction = 260
    elif max_val == 6:
        prediction = 280
    elif max_val == 7:
        prediction = 300
    elif max_val == 8:
        prediction = 320
    elif max_val == 9:
        prediction = 340
    elif max_val == 10:
        prediction = 360
    elif max_val == 11:
        prediction = 380
    elif max_val == 12:
        prediction = 400
    elif max_val == 13:
        prediction = 420
    elif max_val == 14:
        prediction = 440
    elif max_val == 15:
        prediction = 460

    return str(prediction)

if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=8020)