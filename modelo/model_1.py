#%% Librerias
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
from pgmpy.estimators import BayesianEstimator
from pgmpy.sampling import BayesianModelSampling
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from sklearn.metrics import accuracy_score, confusion_matrix
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import numpy as np

#%% Red bayesiana para predecir el éxito académico

# Estructura de la red
model_success = BayesianNetwork([('cole_area_ubicacion','punt_total'), ('cole_bilingue','punt_total'),
                  ('edad_presentacion','punt_total'), ('estu_genero','punt_total'),
                  ('fami_educacionmadre_cod','punt_total'), ('fami_educacionpadre_cod','punt_total'),
                  ('fami_estratovivienda','punt_total'), ('fami_personashogar','punt_total'), ('fami_tienecomputador','punt_total'),
                  ('fami_tieneinternet','punt_total')])

# Subir csv
data_model = pd.read_csv("C:/Users/jd.umana10/Documents/GitHub/predictor_saber11/data/data_model.csv")

# Dividir datos en train y test
X_train, X_test = train_test_split(data_model, random_state=42)

# Emplear el módulo de ajuste de pgmpy para ajustar la CPDs del nuevo modelo
emv_success = MaximumLikelihoodEstimator(model = model_success, data = X_train)

# Obtener las CPDs ajustadas
cpds = emv_success.get_parameters()

print("Calculando cpds...")
cpdem_cole_area_ubicacion = emv_success.estimate_cpd (node = 'cole_area_ubicacion')
cpdem_cole_bilingue = emv_success.estimate_cpd (node = 'cole_bilingue')
cpdem_edad_presentacion = emv_success.estimate_cpd (node = 'edad_presentacion')
cpdem_estu_genero = emv_success.estimate_cpd (node = 'estu_genero')
cpdem_fami_educacionmadre_cod = emv_success.estimate_cpd (node = 'fami_educacionmadre_cod')
cpdem_fami_educacionpadre_cod = emv_success.estimate_cpd (node = 'fami_educacionpadre_cod')
cpdem_fami_estratovivienda = emv_success.estimate_cpd (node = 'fami_estratovivienda')
cpdem_fami_personashogar = emv_success.estimate_cpd (node = 'fami_personashogar')
cpdem_fami_tienecomputador = emv_success.estimate_cpd (node = 'fami_tienecomputador')
cpdem_fami_tieneinternet = emv_success.estimate_cpd (node = 'fami_tieneinternet')
cpdem_punt_total = emv_success.estimate_cpd (node = 'punt_total')

#Asociar las CPDs al modelo
model_success.add_cpds(cpdem_cole_area_ubicacion,
                       cpdem_cole_bilingue,
                       cpdem_edad_presentacion,
                       cpdem_estu_genero,
                       cpdem_fami_educacionmadre_cod,
                       cpdem_fami_educacionpadre_cod,
                       cpdem_fami_estratovivienda,
                       cpdem_fami_personashogar,
                       cpdem_fami_tienecomputador,
                       cpdem_fami_tieneinternet,
                       cpdem_punt_total)

#Revisar que el modelo esté completo
print("Modelo completo:",model_success.check_model())

# Crear un objeto de inferencia
inference = VariableElimination(model_success)

def make_predictions(inference):

    # Crear una lista para guardar las predicciones
    predictions = []

    for _, row in X_test.iterrows():

        # Crear un diccionario de evidencias con los datos de cada fila en datos de prueba
        evidence = {variable: row[variable] for variable in row.index if variable!='punt_total'}
        # Realizar la inferencia para obtener la CPD de "success" dado la evidencia
        try:
            result = inference.query(variables=['punt_total'], evidence=evidence)
            list_result = list(result.values)
            max_val = list_result.index(max(result.values))
            if max_val == 0:
                predictions.append(160)
            elif max_val == 1:
                predictions.append(180)
            elif max_val == 2:
                predictions.append(200)
            elif max_val == 3:
                predictions.append(220)
            elif max_val == 4:
                predictions.append(240)
            elif max_val == 5:
                predictions.append(260)
            elif max_val == 6:
                predictions.append(280)
            elif max_val == 7:
                predictions.append(300)
            elif max_val == 8:
                predictions.append(320)
            elif max_val == 9:
                predictions.append(340)
            elif max_val == 10:
                predictions.append(360)
            elif max_val == 11:
                predictions.append(380)
            elif max_val == 12:
                predictions.append(400)
            elif max_val == 13:
                predictions.append(420)
            elif max_val == 14:
                predictions.append(440)
            elif max_val == 15:
                predictions.append(480)
        except:
            predictions.append('NaN')

    # Obtener el ground truth para comparar las predicciones
    y_true = X_test['punt_total'].tolist()

    # Calcular la exactitud del modelo
    accuracy = accuracy_score(y_true, predictions)
    print(f'Exactitud (Accuracy): {accuracy}')

    # Calcular la matriz de confusión
    confusion = confusion_matrix(y_true, predictions)
    

    return accuracy

if __name__ == "__main__":
    accuracy_model = make_predictions(inference)

import pickle
filename='C:/Users/jd.umana10/Documents/GitHub/predictor_academico_2/aprendizaje_estructura/model.pkl'
with open(filename,'wb') as file:
    pickle.dump(model_success, file)
    file.close()