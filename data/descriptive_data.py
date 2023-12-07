import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def cargar_datos(ruta_archivo):
    """Carga los datos desde un archivo CSV."""
    try:
        datos = pd.read_excel(ruta_archivo)
        return datos
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return None

def estadisticas_descriptivas(datos):
    """Imprime las estadísticas descriptivas básicas del DataFrame."""
    try:
        descripciones = datos.describe(include='all')
        print(descripciones)
    except Exception as e:
        print(f"Error al calcular estadísticas descriptivas: {e}")

def graficar_distribuciones(datos, columnas):
    """Grafica las distribuciones para columnas específicas."""
    for columna in columnas:
        if datos[columna].dtype == 'object':
            # Para datos categóricos, usa un gráfico de barras
            plt.figure(figsize=(10, 5))
            sns.countplot(y=columna, data=datos)
            plt.title(f'Distribución de {columna}')
            plt.show()
        else:
            # Para datos numéricos, usa un histograma
            plt.figure(figsize=(10, 5))
            sns.histplot(datos[columna], kde=True)
            plt.title(f'Distribución de {columna}')
            plt.show()

def main():
    ruta_archivo = 'data_raw.xlsx'
    datos = cargar_datos(ruta_archivo)
    
    if datos is not None:
        estadisticas_descriptivas(datos)
        
        # Lista de columnas para graficar
        columnas_para_graficar = ['punt_ingles', 'punt_matematicas', 'punt_sociales_ciudadanas', 'punt_c_naturales', 'punt_lectura_critica']
        graficar_distribuciones(datos, columnas_para_graficar)

if __name__ == "__main__":
    main()

