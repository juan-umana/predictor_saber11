import pandas as pd

df = pd.read_csv("C:/Users/jd.umana10/Documents/GitHub/predictor_saber11/data/data_model.csv")
print(df.head())
print(df.describe())
print(df.columns)

excluded_edges_1 = [
    # No deben existir enlaces hacia el año en el que se presentó el examen
                  ('cole_area_ubicacion','ano'), ('cole_bilingue','ano'), ('cole_genero','ano'), ('cole_jornada','ano'),
                  ('edad_presentacion','ano'), ('estu_genero','ano'), ('fami_cuartoshogar','ano'),
                  ('fami_educacionmadre_cod','ano'), ('fami_educacionpadre_cod','ano'),
                  ('fami_estratovivienda','ano'), ('fami_personashogar','ano'), ('fami_tienecomputador','ano'),
                  ('fami_tieneinternet','ano'), ('punt_ingles','ano'), ('punt_matematicas','ano'),
                  ('punt_sociales_ciudadanas','ano'), ('punt_c_naturales','ano'),
                  ('punt_lectura_critica','ano'),
    # No deben existir enlaces hacia el genero del estudiante
                  ('cole_area_ubicacion','estu_genero'), ('cole_bilingue','estu_genero'), ('cole_genero','estu_genero'), ('cole_jornada','estu_genero'),
                  ('edad_presentacion','estu_genero'), ('ano','estu_genero'), ('fami_cuartoshogar','estu_genero'),
                  ('fami_educacionmadre_cod','estu_genero'), ('fami_educacionpadre_cod','estu_genero'),
                  ('fami_estratovivienda','estu_genero'), ('fami_personashogar','estu_genero'), ('fami_tienecomputador','estu_genero'),
                  ('fami_tieneinternet','estu_genero'), ('punt_ingles','estu_genero'), ('punt_matematicas','estu_genero'),
                  ('punt_sociales_ciudadanas','estu_genero'), ('punt_c_naturales','estu_genero'),
                  ('punt_lectura_critica','estu_genero')]

from pgmpy.estimators import HillClimbSearch
from pgmpy.estimators import BicScore

scoring_method = BicScore(data=df)
esth_1 = HillClimbSearch(data=df)
estimated_modelh_1 = esth_1.estimate(
    scoring_method=scoring_method,
    black_list=excluded_edges_1, max_iter=int(1e4)
)
print(estimated_modelh_1)
print(estimated_modelh_1.nodes())
print(estimated_modelh_1.edges())

print(scoring_method.score(estimated_modelh_1))

# Visualization https://public.flourish.studio/visualisation/15582966/

excluded_edges_2 = [
    # No deben existir enlaces hacia el año en el que se presentó el examen
                  ('cole_area_ubicacion','ano'), ('cole_bilingue','ano'), ('cole_genero','ano'), ('cole_jornada','ano'),
                  ('edad_presentacion','ano'), ('estu_genero','ano'), ('fami_cuartoshogar','ano'),
                  ('fami_educacionmadre_cod','ano'), ('fami_educacionpadre_cod','ano'),
                  ('fami_estratovivienda','ano'), ('fami_personashogar','ano'), ('fami_tienecomputador','ano'),
                  ('fami_tieneinternet','ano'), ('punt_ingles','ano'), ('punt_matematicas','ano'),
                  ('punt_sociales_ciudadanas','ano'), ('punt_c_naturales','ano'),
                  ('punt_lectura_critica','ano'),
    # No deben existir enlaces hacia el genero del estudiante
                  ('cole_area_ubicacion','estu_genero'), ('cole_bilingue','estu_genero'), ('cole_genero','estu_genero'), ('cole_jornada','estu_genero'),
                  ('edad_presentacion','estu_genero'), ('ano','estu_genero'), ('fami_cuartoshogar','estu_genero'),
                  ('fami_educacionmadre_cod','estu_genero'), ('fami_educacionpadre_cod','estu_genero'),
                  ('fami_estratovivienda','estu_genero'), ('fami_personashogar','estu_genero'), ('fami_tienecomputador','estu_genero'),
                  ('fami_tieneinternet','estu_genero'), ('punt_ingles','estu_genero'), ('punt_matematicas','estu_genero'),
                  ('punt_sociales_ciudadanas','estu_genero'), ('punt_c_naturales','estu_genero'),
                  ('punt_lectura_critica','estu_genero'),
    # No deben existir enlaces hacia el genero del estudiante
                  ('punt_ingles','punt_matematicas'), ('punt_ingles','punt_sociales_ciudadanas'),('punt_ingles','punt_c_naturales'),('punt_ingles','punt_lectura_critica'),
                  ('punt_matematicas','punt_ingles'), ('punt_matematicas','punt_sociales_ciudadanas'),('punt_matematicas','punt_c_naturales'),('punt_matematicas','punt_lectura_critica'),
                  ('punt_sociales_ciudadanas','punt_ingles'), ('punt_sociales_ciudadanas','punt_matematicas'), ('punt_sociales_ciudadanas','punt_c_naturales'),('punt_sociales_ciudadanas','punt_lectura_critica'),
                  ('punt_c_naturales','punt_ingles'), ('punt_c_naturales', 'punt_matematicas'), ('punt_c_naturales','punt_sociales_ciudadanas'), ('punt_c_naturales','punt_lectura_critica'),
                  ('punt_lectura_critica','punt_ingles'), ('punt_lectura_critica','punt_matematicas'), ('punt_lectura_critica','punt_sociales_ciudadanas'), ('punt_lectura_critica','punt_c_naturales')]

from pgmpy.estimators import HillClimbSearch
from pgmpy.estimators import BicScore

scoring_method = BicScore(data=df)
esth_2 = HillClimbSearch(data=df)
estimated_modelh_2 = esth_2.estimate(
    scoring_method=scoring_method,
    black_list=excluded_edges_2, max_iter=int(1e4)
)
print(estimated_modelh_2)
print(estimated_modelh_2.nodes())
print(estimated_modelh_2.edges())

print(scoring_method.score(estimated_modelh_2))
breakpoint()