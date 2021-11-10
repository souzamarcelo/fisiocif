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
    data['considera_importante'] = data['considera_importante'].map(lambda x: 'S' if x == 'SIM' else 'N')
    data['entende_importancia'] = data['entende_importancia'].map(lambda x: 'S' if x == 'SIM' else 'N')
    data['preparado'] = data['preparado'].map(lambda x: 'N' if 'Não' in x else 'S')
    data['como_conheceu'] = data['como_conheceu'].map(lambda x: 'faculdade' if 'faculdade' in x else 'N' if 'Não' in x else 'eventos' if 'eventos' in x else 'X')
    data['idade'] = data['idade'].map(lambda x: x.replace(' anos', ''))
    data['instituicao'] = data['instituicao'].map(lambda x: 'publica' if x == 'UNICENTRO' else 'privada')
    return data

def aggregate_sample(data, col):
    total = len(data)
    table = data.copy()
    table['n'] = 1
    table['percentual'] = 1
    table = table.groupby([col], as_index = False).agg({'n': 'count', 'percentual': 'count'})
    table['percentual'] = table['percentual'].map(lambda x: round(100 * x / total, 1))
    table['variavel'] = col
    table['valores'] = table[col]
    table = table[['variavel', 'valores', 'n', 'percentual']]
    return table

def table_sample_students(data):
    table_idade = aggregate_sample(data, 'idade')
    table_sexo = aggregate_sample(data, 'sexo')
    table_periodo = aggregate_sample(data, 'periodo')
    table = pd.concat([table_idade, table_sexo, table_periodo])
    return table

def table_sample_cif_students(data):
    tables = []
    tables.append(aggregate_sample(data, 'conhece'))
    tables.append(aggregate_sample(data, 'conhece_cif_cj'))
    tables.append(aggregate_sample(data, 'conhece_core_sets'))
    tables.append(aggregate_sample(data, 'usa'))
    tables.append(aggregate_sample(data, 'motivo_nao_usa'))
    tables.append(aggregate_sample(data, 'treinamento'))
    tables.append(aggregate_sample(data, 'conhecimento'))
    tables.append(aggregate_sample(data, 'considera_importante'))
    tables.append(aggregate_sample(data, 'entende_importancia'))
    table = pd.concat(tables)
    return table

def plot_institution(data):
    data['conhece_s'] = data['conhece'].map(lambda x: 1 if x == 'S' else 0)
    data['conhece_n'] = data['conhece'].map(lambda x: 1 if x == 'N' else 0)
    data['usa_s'] = data['usa'].map(lambda x: 1 if x == 'S' else 0)
    data['usa_n'] = data['usa'].map(lambda x: 1 if x == 'N' else 0)
    data['importante_s'] = data['considera_importante'].map(lambda x: 1 if x == 'S' else 0)
    data['importante_n'] = data['considera_importante'].map(lambda x: 1 if x == 'N' else 0)
    data = data.groupby('instituicao', as_index = False).agg({'conhece_s': 'sum', 'conhece_n': 'sum', 'usa_s': 'sum', 'usa_n': 'sum', 'importante_s': 'sum', 'importante_n': 'sum'})
    
    publica_sim = [
        data[data['instituicao'] == 'publica']['conhece_s'].unique()[0],
        data[data['instituicao'] == 'publica']['importante_s'].unique()[0],
        data[data['instituicao'] == 'publica']['usa_s'].unique()[0]
    ]
    publica_nao = [
        data[data['instituicao'] == 'publica']['conhece_n'].unique()[0],
        data[data['instituicao'] == 'publica']['importante_n'].unique()[0],
        data[data['instituicao'] == 'publica']['usa_n'].unique()[0]
    ]
    privada_sim = [
        data[data['instituicao'] == 'privada']['conhece_s'].unique()[0],
        data[data['instituicao'] == 'privada']['importante_s'].unique()[0],
        data[data['instituicao'] == 'privada']['usa_s'].unique()[0]
    ]
    privada_nao = [
        data[data['instituicao'] == 'privada']['conhece_n'].unique()[0],
        data[data['instituicao'] == 'privada']['importante_n'].unique()[0],
        data[data['instituicao'] == 'privada']['usa_n'].unique()[0]
    ]

    fig = plt.figure()
    labels = ['Conhece', 'Considera\nimportante', 'Usa']
    width = 0.8

    ax = fig.add_subplot(1, 2, 1)
    ax.set_ylim(0, 50)
    ax.bar(labels, publica_sim, width, label = 'Sim')
    ax.bar(labels, publica_nao, width, bottom = publica_sim, label = 'Não')
    ax.set_ylabel('Quantidade')
    ax.set_title('Instituições públicas')
    ax.legend()

    ax = fig.add_subplot(1, 2, 2)
    ax.set_ylim(0, 50)
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position('right')
    ax.bar(labels, privada_sim, width, label = 'Sim')
    ax.bar(labels, privada_nao, width, bottom = privada_sim, label = 'Não')
    ax.set_ylabel('Quantidade')
    ax.set_title('Instituições privadas')
    ax.legend()

    fig.tight_layout()
    return plt

def plot_year(data):
    data['conhece_s'] = data['conhece'].map(lambda x: 1 if x == 'S' else 0)
    data['conhece_n'] = data['conhece'].map(lambda x: 1 if x == 'N' else 0)
    data['usa_s'] = data['usa'].map(lambda x: 1 if x == 'S' else 0)
    data['usa_n'] = data['usa'].map(lambda x: 1 if x == 'N' else 0)
    data['importante_s'] = data['considera_importante'].map(lambda x: 1 if x == 'S' else 0)
    data['importante_n'] = data['considera_importante'].map(lambda x: 1 if x == 'N' else 0)
    data = data.groupby('periodo', as_index = False).agg({'conhece_s': 'sum', 'conhece_n': 'sum', 'usa_s': 'sum', 'usa_n': 'sum', 'importante_s': 'sum', 'importante_n': 'sum'})
    
    sim_3 = [
        data[data['periodo'] == 3]['conhece_s'].unique()[0],
        data[data['periodo'] == 3]['importante_s'].unique()[0],
        data[data['periodo'] == 3]['usa_s'].unique()[0]
    ]
    nao_3 = [
        data[data['periodo'] == 3]['conhece_n'].unique()[0],
        data[data['periodo'] == 3]['importante_n'].unique()[0],
        data[data['periodo'] == 3]['usa_n'].unique()[0]
    ]
    sim_4 = [
        data[data['periodo'] == 4]['conhece_s'].unique()[0],
        data[data['periodo'] == 4]['importante_s'].unique()[0],
        data[data['periodo'] == 4]['usa_s'].unique()[0]
    ]
    nao_4 = [
        data[data['periodo'] == 4]['conhece_n'].unique()[0],
        data[data['periodo'] == 4]['importante_n'].unique()[0],
        data[data['periodo'] == 4]['usa_n'].unique()[0]
    ]
    sim_5 = [
        data[data['periodo'] == 5]['conhece_s'].unique()[0],
        data[data['periodo'] == 5]['importante_s'].unique()[0],
        data[data['periodo'] == 5]['usa_s'].unique()[0]
    ]
    nao_5 = [
        data[data['periodo'] == 5]['conhece_n'].unique()[0],
        data[data['periodo'] == 5]['importante_n'].unique()[0],
        data[data['periodo'] == 5]['usa_n'].unique()[0]
    ]

    fig = plt.figure()
    labels = ['Conhece', 'Considera\nimportante', 'Usa']
    width = 0.8
    max_lim = 40

    ax = fig.add_subplot(1, 3, 1)
    ax.set_ylim(0, max_lim)
    ax.bar(labels, sim_3, width, label = 'Sim')
    ax.bar(labels, nao_3, width, bottom = sim_3, label = 'Não')
    ax.set_ylabel('Quantidade')
    ax.set_title('3º ano')
    ax.legend()

    ax = fig.add_subplot(1, 3, 2)
    ax.set_ylim(0, max_lim)
    #ax.yaxis.tick_right()
    #ax.yaxis.set_label_position('right')
    ax.bar(labels, sim_4, width, label = 'Sim')
    ax.bar(labels, nao_4, width, bottom = sim_4, label = 'Não')
    ax.get_yaxis().set_visible(False)
    ax.set_title('4º ano')
    ax.legend()
    
    ax = fig.add_subplot(1, 3, 3)
    ax.set_ylim(0, max_lim)
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position('right')
    ax.bar(labels, sim_5, width, label = 'Sim')
    ax.bar(labels, nao_5, width, bottom = sim_5, label = 'Não')
    ax.set_ylabel('Quantidade')
    ax.set_title('5º ano')
    ax.legend()

    fig.set_size_inches(8.5, 4)
    fig.tight_layout()
    return plt

def plot_knowledge(data):
    com = []
    sem = []
    com.append(len(data[(data['treinamento'] == 'S') & (data['conhecimento'] == 'Muito ruim')]))
    com.append(len(data[(data['treinamento'] == 'S') & (data['conhecimento'] == 'Ruim')]))
    com.append(len(data[(data['treinamento'] == 'S') & (data['conhecimento'] == 'Razoável')]))
    com.append(len(data[(data['treinamento'] == 'S') & (data['conhecimento'] == 'Bom')]))
    com.append(len(data[(data['treinamento'] == 'S') & (data['conhecimento'] == 'Muito bom')]))
    sem.append(len(data[(data['treinamento'] == 'N') & (data['conhecimento'] == 'Muito ruim')]))
    sem.append(len(data[(data['treinamento'] == 'N') & (data['conhecimento'] == 'Ruim')]))
    sem.append(len(data[(data['treinamento'] == 'N') & (data['conhecimento'] == 'Razoável')]))
    sem.append(len(data[(data['treinamento'] == 'N') & (data['conhecimento'] == 'Bom')]))
    sem.append(len(data[(data['treinamento'] == 'N') & (data['conhecimento'] == 'Muito bom')]))

    fig = plt.figure()
    ax = plt.gca()

    labels = ['Muito ruim', 'Ruim', 'Razoável', 'Bom', 'Muito bom']
    x = np.arange(len(labels))
    width = 0.35

    rects1 = ax.bar(x - width/2, sem, width, label = 'Sem treinamento', color = 'red')
    rects2 = ax.bar(x + width/2, com, width, label = 'Com treinamento', color = 'green')

    ax.set_ylabel('Quantidade')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding = 2)
    ax.bar_label(rects2, padding = 2)

    fig.tight_layout()
    return plt

def plot_reason(data):
    com = []
    sem = []
    com.append(len(data[(data['treinamento'] == 'S') & (data['motivo_nao_usa'] == 'Não conhecia essa classificação')]))
    com.append(len(data[(data['treinamento'] == 'S') & (data['motivo_nao_usa'] == 'Tenho dificuldades para entender a CIF')]))
    com.append(len(data[(data['treinamento'] == 'S') & (data['motivo_nao_usa'] == 'Tenho dificuldades para aplicar a CIF')]))
    com.append(len(data[(data['treinamento'] == 'S') & (data['motivo_nao_usa'] == 'Eu uso a CIF')]))
    sem.append(len(data[(data['treinamento'] == 'N') & (data['motivo_nao_usa'] == 'Não conhecia essa classificação')]))
    sem.append(len(data[(data['treinamento'] == 'N') & (data['motivo_nao_usa'] == 'Tenho dificuldades para entender a CIF')]))
    sem.append(len(data[(data['treinamento'] == 'N') & (data['motivo_nao_usa'] == 'Tenho dificuldades para aplicar a CIF')]))
    sem.append(len(data[(data['treinamento'] == 'N') & (data['motivo_nao_usa'] == 'Eu uso a CIF')]))

    fig = plt.figure()
    ax = plt.gca()

    labels = ['Não conhece', 'Dificuldade\npara entender', 'Dificuldade\npara aplicar', 'Usa']
    x = np.arange(len(labels))
    width = 0.35

    rects1 = ax.bar(x - width/2, sem, width, label = 'Sem treinamento', color = 'red')
    rects2 = ax.bar(x + width/2, com, width, label = 'Com treinamento', color = 'green')

    ax.set_ylabel('Quantidade')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.bar_label(rects1, padding = 2)
    ax.bar_label(rects2, padding = 2)

    fig.tight_layout()
    return plt

#data = read_data_students()
#plot_year(data)