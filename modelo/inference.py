import pickle

# Read model from PKL file 
filename='C:/Users/jd.umana10/Documents/GitHub/predictor_saber11/modelo/model.pkl'
file = open(filename, 'rb')
model_success = pickle.load(file)
file.close()


# Print model 
print(model_success)

# Check_model check for the model structure and the associated CPD and returns True if everything is correct otherwise throws an exception
print(model_success.check_model())

# Infering the posterior probability
from pgmpy.inference import VariableElimination

infer = VariableElimination(model_success)

evidence = {'cole_area_ubicacion': 'URBANO', 'cole_bilingue': 'S',
            'edad_presentacion': 20, 'estu_genero': 'M', 'fami_educacionmadre_cod': 10,
            'fami_educacionpadre_cod': 10, 'fami_estratovivienda': 'Estrato 6', 'fami_personashogar': '5 a 6',
            'fami_tienecomputador': 'Si', 'fami_tieneinternet': 'Si'} 

posterior_p = infer.query(['punt_total'], evidence=evidence)
print(posterior_p)