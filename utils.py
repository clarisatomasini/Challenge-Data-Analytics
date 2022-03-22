from datetime import datetime
import logging
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from decouple import config

CONNECTION_DB = config('DATABASE_URL')

def search_link_in_page(page, condition) -> str:
    logger = logging.getLogger(__name__)
    link = ''
    try:
        request = requests.get(page)
        if request.status_code != requests.codes.ok:
            request.raise_for_status()

        soup = BeautifulSoup(request.content, 'html.parser')
        link = soup.select(condition)[0].get('href')
    except Exception:
        logger.error("Request failed", exc_info=True)
    else:   
        logger.info('Request: %d "%s"', request.status_code, request.url)
        return link


def download_dataset(url) -> str:
    logger = logging.getLogger(__name__)
    data = ''
        
    try:
        request = requests.get(url)
        if request.status_code != requests.codes.ok:
            request.raise_for_status()

        request.encoding = 'utf-8'
        data = request.text
    except Exception:
        logger.error("Download failed", exc_info=True)
    else:
        logger.info('Request: %d "%s"', request.status_code, request.url)
        return data
    
def save_as_csv(path, data) -> bool:
    logger = logging.getLogger(__name__)

    try:   
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        
        with open(path, 'w', encoding='UTF8', newline='') as file:
            file.write(data)

    except Exception:
        logger.error("Save file failed", exc_info=True)
        return False
    else:
        logger.info('Save file: "%s"', path)
        return True

def get_normed_data(path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.rename(normed_colnames, axis='columns', inplace=True)

    for col in COL_NAMES:
        if col not in df.columns:
            df[col] = None
       
    return df

def normed_colnames(x):
    x_lower = x.lower()
    
    if x_lower == 'cod_loc':
        return 'cod_localidad'
    
    if x_lower == 'idprovincia':
        return 'id_provincia'
    
    if x_lower == 'iddepartamento':
        return 'id_departamento'
    
    if x_lower in ['direccion', 'dirección']:
        return 'domicilio'

    if x_lower == 'cp':
        return 'codigo_postal'
    
    if x_lower in ['telefono', 'teléfono']:
        return 'numero_telefono'
    
    if x_lower == 'categoría':
        return 'categoria'
    
    return x_lower

def get_info_cines(df) -> pd.DataFrame:
    info_cines = df.groupby(by=['provincia'])[['pantallas', 'butacas', 'espacio_incaa']].sum().reset_index()
    return info_cines

def get_count_reg(df) -> pd.DataFrame:
    registros = df.groupby(by=['provincia', 'categoria', 'fuente']).nombre.nunique().reset_index()
    
    registros.rename(columns={'nombre': 'cantidad'}, inplace=True)
    return registros

def get_data(pd) -> pd.DataFrame:
    return pd[COL_NAMES].copy()

def save_in_db(df, table_name):
    logger = logging.getLogger(__name__)

    df['fecha_carga'] = datetime.today()
    try:
        engine = create_engine(CONNECTION_DB, echo_pool=True)
        with engine.begin() as db_conn:
            df.to_sql(table_name, con=db_conn, if_exists='replace')

    except Exception as e:
        logger.error(f'Connect DB: {e}')
    else:
        logger.info('Save %d rows in table "%s"', len(df), table_name)


COL_NAMES = [
    'cod_localidad', 
    'id_provincia', 
    'id_departamento', 
    'categoria', 
    'provincia', 
    'localidad',
    'nombre', 
    'domicilio', 
    'codigo_postal', 
    'numero_telefono', 
    'mail', 
    'web'
    ]