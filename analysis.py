import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def read_data_students():
    data = pd.read_csv('./data/estudantes.csv', sep = ',')
    cols = list(data.columns)
    cols.remove('data_hora')
    cols.remove('declaracao')
    cols.remove('nome')
    cols.remove('video_ajudou')
    data = data[cols]
    data['sexo'] = data['sexo'].map(lambda x: 'F' if x == 'Feminino' else 'M')
    data['periodo'] = data['periodo'].map(lambda x: 3 if '3' in x else 4 if '4' in x else 5 if '5' in x else 'X')
    data['conhece'] = data['conhece'].map(lambda x: 'S' if x == 'SIM' else 'N')
    data['usa'] = data['usa'].map(lambda x: 'S' if x == 'SIM' else 'N')
    data['treinamento'] = data['treinamento'].map(lambda x: 'S' if x == 'SIM' else 'N')
    data['conhece_cif_cj'] = data['conhece_cif_cj'].map(lambda x: 'S' if x == 'SIM' else 'N')
    data['conhece_core_sets'] = data['conhece_core_sets'].map(lambda x: 'S' if x == 'SIM' else 'N')
    data['considera_importance'] = data['considera_importance'].map(lambda x: 'S' if x == 'SIM' else 'N')
    data['entende_importancia'] = data['entende_importancia'].map(lambda x: 'S' if x == 'SIM' else 'N')
    data['preparado'] = data['preparado'].map(lambda x: 'N' if 'Não' in x else 'S')
    data['como_conheceu'] = data['como_conheceu'].map(lambda x: 'faculdade' if 'faculdade' in x else 'N' if 'Não' in x else 'eventos' if 'eventos' in x else 'X')
    data['idade'] = data['idade'].map(lambda x: x.replace(' anos', ''))
    data['instituicao'] = data['instituicao'].map(lambda x: 'publica' if x == 'UNICENTRO' else 'privada')
    return data

def table_sample_students(data):
    total = len(data)
    table = data.copy()
    table['n'] = 1
    table['percentual'] = 1
    table_idade = table.groupby(['idade'], as_index = False).agg({'n': 'count', 'percentual': 'count'})
    table_idade['percentual'] = table_idade['percentual'].map(lambda x: round(100 * x / total, 1))
    table_idade['variavel'] = 'idade'
    table_idade['valores'] = table_idade['idade']
    table_idade = table_idade[['variavel', 'valores', 'n', 'percentual']]
    table_sexo = table.groupby(['sexo'], as_index = False).agg({'n': 'count', 'percentual': 'count'})
    table_sexo['percentual'] = table_sexo['percentual'].map(lambda x: round(100 * x / total, 1))
    table_sexo['variavel'] = 'sexo'
    table_sexo['valores'] = table_sexo['sexo']
    table_sexo = table_sexo[['variavel', 'valores', 'n', 'percentual']]
    table_periodo = table.groupby(['periodo'], as_index = False).agg({'n': 'count', 'percentual': 'count'})
    table_periodo['percentual'] = table_periodo['percentual'].map(lambda x: round(100 * x / total, 1))
    table_periodo['variavel'] = 'periodo'
    table_periodo['valores'] = table_periodo['periodo']
    table_periodo = table_periodo[['variavel', 'valores', 'n', 'percentual']]
    table = pd.concat([table_idade, table_sexo, table_periodo])
    return table

# def table_sample_students(data):
#     total = len(data)
#     table = data.copy()
#     table['n'] = 1
#     table['percentual'] = 1
#     table_idade = table.groupby(['idade'], as_index = False).agg({'n': 'count', 'percentual': 'count'})
#     table_idade['percentual'] = table_idade['percentual'].map(lambda x: round(100 * x / total, 1))
#     table_sexo = table.groupby(['sexo'], as_index = False).agg({'n': 'count', 'percentual': 'count'})
#     table_sexo['percentual'] = table_sexo['percentual'].map(lambda x: round(100 * x / total, 1))
#     table_periodo = table.groupby(['periodo'], as_index = False).agg({'n': 'count', 'percentual': 'count'})
#     table_periodo['percentual'] = table_periodo['percentual'].map(lambda x: round(100 * x / total, 1))
#     return table_idade, table_sexo, table_periodo

def table_sample_cif_students(data):
    total = len(data)
    table = data.copy()
    table['n'] = 1
    table['percentual'] = 1

# def plot_institution(data):
#     total_publica = data[data['instituicao'] == 'publica']['instituicao'].count()
#     total_privada = data[data['instituicao'] == 'privada']['instituicao'].count()
#     data['conhece_s'] = data['conhece'].map(lambda x: 1 if x == 'S' else 0)
#     data['conhece_n'] = data['conhece'].map(lambda x: 1 if x == 'N' else 0)
#     data['usa_s'] = data['usa'].map(lambda x: 1 if x == 'S' else 0)
#     data['usa_n'] = data['usa'].map(lambda x: 1 if x == 'N' else 0)
#     data = data.groupby('instituicao', as_index = False).agg({'conhece_s': 'sum', 'conhece_n': 'sum', 'usa_s': 'sum', 'usa_n': 'sum'})
#     data.loc[data['instituicao'] == 'publica', 'conhece_s'] = data[data['instituicao'] == 'publica']['conhece_s'].map(lambda x: 100 * x / total_publica)
#     data.loc[data['instituicao'] == 'publica', 'conhece_n'] = data[data['instituicao'] == 'publica']['conhece_n'].map(lambda x: 100 * x / total_publica)
#     data.loc[data['instituicao'] == 'privada', 'conhece_s'] = data[data['instituicao'] == 'privada']['conhece_s'].map(lambda x: 100 * x / total_privada)
#     data.loc[data['instituicao'] == 'privada', 'conhece_n'] = data[data['instituicao'] == 'privada']['conhece_n'].map(lambda x: 100 * x / total_privada)
    
#     plt.bar(data['instituicao'], data['conhece_s'])
#     plt.bar(data['instituicao'], data['conhece_n'])
#     plt.show()

#data = read_data_students()
#table_sample_cif_students(data)
#table_sample_students(data)
#exit()