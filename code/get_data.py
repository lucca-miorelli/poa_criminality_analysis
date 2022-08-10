import pandas as pd

def extract(url:str):

    use_cols = ['Data Fato', 'Grupo Fato',
        'Tipo Enquadramento', 'Tipo Fato', 'Municipio Fato', 'Local Fato',
        'Bairro', 'Quantidade Vítimas', 'Idade Vítima', 'Sexo Vítima']

    df = pd.read_csv(filepath_or_buffer=url,
                    usecols=use_cols,
                    sep=';')
    
    return df

def filter_poa(df:pd.DataFrame):

    return df[df['Municipio Fato'] == 'PORTO ALEGRE']

def rename_columns(df:pd.DataFrame):
    df.rename(columns={
        'Data Fato' : 'data_fato',
        'Grupo Fato': 'grupo_fato',
        'Tipo Enquadramento' : 'tipo_enquadramento',
        'Tipo Fato' : 'tipo_fato',
        'Municipio Fato' : 'municipio_fato',
        'Local Fato' : 'local_fato',
        'Bairro' : 'bairro',
        'Quantidade Vítimas' : 'qtd_vitimas',
        'Idade Vítima': 'idade_vitima',
        'Sexo Vítima' : 'sexo_vitima'
    }, inplace=True)

    return df

def cols_transformation(df:pd.DataFrame):

    df.reset_index(inplace=True, drop=True)
    df['data_fato'] = pd.to_datetime(df['data_fato'], format='%d/%m/%Y')
    df['bairro'] = df['bairro'].map(lambda x: x.lower() if type(x) == str else x)

    return df


def transform(df:pd.DataFrame):

    df = cols_transformation(
        rename_columns(
            filter_poa(df)
        )
    )

    df_poa = pd.DataFrame(df.groupby('data_fato')[['tipo_enquadramento', 'bairro']].count().rename(columns={'tipo_enquadramento':'count', 'bairro':'bairro'})).drop(columns='bairro')
    df_poa['mv_avg_7d'] = df_poa['count'].rolling(7).mean()
    df_poa['date'] = df_poa.index.values

    return df_poa