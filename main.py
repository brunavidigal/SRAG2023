# @Time     : Ago. 24, 2025
# @Author   : Bruna Rodrigues Vidigal
# @FileName : main.py
# @Version  : 1.0
# @Project  : SRAG2023
# @IDE      : PyCharm

##  libraries and configs

import pandas as pd

pd.set_option('display.max_rows', None)


## development


def upload_data(path):
    """
    :param path: str, the file path to the CSV file
    :return: pandas DataFrame containing the data from the CSV file
    """
    return pd.read_csv(path, delimiter=';')


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

    return dataframe


if __name__ == '__main__':
    df = upload_data('C:/Users/bruni/PycharmProjects/PythonProject/SRAG2023/INFLUD23-26-06-2025.csv')
    df = missing_data(df, 60)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
