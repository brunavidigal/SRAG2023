# @Time     : Ago. 24, 2025
# @Author   : Bruna Rodrigues Vidigal
# @FileName : main.py
# @Version  : 1.0
# @Project  : SRAG2023
# @IDE      : PyCharm

##  libraries and configs

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns

from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# from tabulate import tabulate

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


## development


def upload_data(path):
    """
    :param path: str, the file path to the CSV file
    :return: pandas DataFrame containing the data from the CSV file
    """
    return pd.read_csv(path,
                       delimiter=';',
                       dtype={'NU_NOTIFIC': str,
                              'CO_MUN_NOT': str
                              },
                       parse_dates=['DT_NOTIFIC'])


def missing_data(dataframe, cut_col):
    """
    :param cut_col:
    :param dataframe:
    :return:
    """
    print(f'O conjunto de dados possui: {dataframe.shape[0]} linhas e {dataframe.shape[1]} colunas \n')
    initial_cols = dataframe.shape[1]

    # remove all columns that are completely null
    dataframe = dataframe.dropna(axis=1, how="all")
    non_null_cols = dataframe.shape[1]
    print(
        f'Foram removidas {initial_cols - non_null_cols} colunas onde todos os valores eram nulos. ({non_null_cols} '
        f'colunas restantes) \n')

    missing_by_cols = (dataframe.isnull().mean() * 100).sort_values(ascending=False)

    # drop columns where over 60% of the data is missing
    valid_columns = [col for col, percent in missing_by_cols.items() if percent <= cut_col]
    dataframe = dataframe[valid_columns]
    last_cols = dataframe.shape[1]
    print(
        f'Foram removidas {non_null_cols - last_cols} colunas onde mais de 60% dos valores eram nulos. ({last_cols} '
        f'colunas restantes) \n')

    # remove rows with missing required or internal data
    dataframe = dataframe.dropna(subset=['SG_UF_NOT', 'CO_MUN_NOT'])

    print(f'O conjunto de dados final possui: {dataframe.shape[0]} linhas e {dataframe.shape[1]} colunas \n')

    return dataframe


def plot_relative_frequency(relative_frequency, column, show=True):
    plt.figure(figsize=(18, 8))
    relative_frequency.plot(kind='bar', color='skyblue', edgecolor='black')

    # plt.title('Frequência Relativa das Categorias', fontsize=20)
    plt.xlabel(column, fontsize=15)
    plt.ylabel('Frequência Relativa', fontsize=18)
    plt.tick_params(labelsize=15)
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.savefig(f'relative_frequency_{column}.png')


def plot_temporal(serie):
    decompose = seasonal_decompose(serie, model='Aditivo')
    fig, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    axes[0].plot(decompose.observed)
    axes[0].set_ylabel('Observado')
    axes[1].plot(decompose.trend)
    axes[1].set_ylabel('Tendência')
    axes[2].plot(decompose.seasonal)
    axes[2].set_ylabel('Sazonal')
    axes[3].plot(decompose.resid)
    axes[3].set_ylabel('Resíduos')

    # plt.suptitle('Decomposição da Série Temporal')
    plt.tight_layout()

    plt.savefig(f'timeseries.png')


def plot_map(geod_df, column):
    fig, ax = plt.subplots(figsize=(18, 8))

    vmin, vmax = geod_df[column].min(), geod_df[column].quantile(.99)
    colors = plt.cm.Reds((geod_df[column] - vmin) / (vmax - vmin))
    geod_df.plot(ax=ax, color=colors, edgecolor='black', linewidth=0.1)
    sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.ax.set_ylabel("Qt. de Notificação", labelpad=-75, va='center', fontsize=16)
    ax.axis('off')

    plt.savefig(f'map_{column}.png')


if __name__ == '__main__':
    df = upload_data('C:/Users/bruni/PycharmProjects/PythonProject/SRAG2023/INFLUD23-26-06-2025.csv')

    # adjust date range to match the target analysis period
    df = df.loc[df['DT_NOTIFIC'].dt.year == 2023]

    # Remove rows where age is less than 0
    df.drop(df[df['NU_IDADE_N'] < 0].index, inplace=True)
    df.drop(df[df['CS_SEXO'] == 'I'].index, inplace=True)

    # categorize age into age groups
    df['NU_IDADE_N'] = np.where(df['TP_IDADE'].isin([1, 2]), 0, df['NU_IDADE_N'])
    bins = [0, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 120]
    labels = [
        '0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39',
        '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+'
    ]
    df['FX_ETARIA'] = pd.cut(df['NU_IDADE_N'], bins=bins, labels=labels, right=True, include_lowest=True)

    # handle missing values
    df = missing_data(df, 60)

    # create column that indetifies the form type
    df['NU_CARACT'] = df['NU_NOTIFIC'].astype(str).str[0].astype(int)
    # print(df['NU_CARACT'].value_counts(normalize=True))

    # columns not found in the data dictionary
    unmaped_columns = ['FAB_COV_2', 'FAB_COV_1', 'CO_DETEC', 'SURTO_SG']
    df.drop(columns=unmaped_columns, inplace=True)

    # relative frequency plots by epidemiological week
    # relative_frequency_columns = ['SEM_NOT', 'SEM_PRI']
    # for col in relative_frequency_columns:
    #     plot_relative_frequency(df[col].value_counts(normalize=True).sort_index(), col)

    # seasonal decompose
    # plot_temporal(df['DT_NOTIFIC'].value_counts().sort_index())

    # map plot
    # df_uf_counts = df['SG_UF_NOT'].value_counts().reset_index()
    # df_uf_counts.columns = ['SG_UF_NOT', 'QTD_UF_NOT']
    # geod_uf = gpd.read_file("C:/Users/bruni/PycharmProjects/PythonProject/SRAG2023/BR_UF_2024.shp")
    # geod_uf = geod_uf.merge(df_uf_counts, how='left', left_on='SIGLA_UF', right_on='SG_UF_NOT')
    # plot_map(geod_uf, column='QTD_UF_NOT')

    df['TARGET_OBITO'] = (df['EVOLUCAO'] == 1).astype(int)

    # Verificamos o mapeamento (geralmente: 0 = 'F', 1 = 'M')
    le = LabelEncoder()
    df['CS_SEXO_COD'] = le.fit_transform(df['CS_SEXO'])
    print(dict(zip(le.classes_, le.transform(le.classes_))))

    # One-Hot Encoding
    idade_dummies = pd.get_dummies(df['FX_ETARIA'], prefix='IDADE')

    X = pd.concat([df[['CS_SEXO_COD']], idade_dummies], axis=1)
    y = df['TARGET_OBITO']

    X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    model = LogisticRegression(random_state=0, class_weight='balanced', max_iter=1000)

    model.fit(X_treino, y_treino)

    predict = model.predict(X_teste)

    # d) Avaliar o modelo
    print("Acurácia:", accuracy_score(y_teste, predict))
    print("\nRelatório de Classificação:\n", classification_report(y_teste, predict))
    print("\nMatriz de Confusão:\n", confusion_matrix(y_teste, predict))

    print('intercept:', model.intercept_)
    print('coef:', model.coef_, end='\n\n')

    sns.heatmap(confusion_matrix(y_teste, predict), cmap='coolwarm', annot=True, linewidth=1, fmt='d')
    plt.savefig(f'confusion_matrix.png')



