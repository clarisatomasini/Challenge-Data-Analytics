from datetime import datetime
import logging
import logging.config
import os
import pandas as pd
import utils 


def load_data():
    site = 'https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/'

    urls = {'museos': 'cultura_4207def0-2ff7-41d5-9095-d42ae8207a5d', \
        'salas_de_cine': 'cultura_392ce1a8-ef11-4776-b280-6f1c7fae16ae',\
        'bibliotecas_populares': 'cultura_01c6c048-dbeb-44e0-8efa-6944f73715d7'}
    
    today = datetime.today()
    list_data = []

    for item in urls:
        dataset_link = utils.search_link_in_page(
                site + urls[item], 
                'div.resource-actions > a[href$=".csv"]')
        text = utils.download_dataset(dataset_link)

        path = os.path.join(item, 
                today.strftime("%Y-%B"),
                f'{item}-{today.strftime("%d-%m-%Y")}.csv')

        if not utils.save_as_csv(path, text):
            continue

        list_data.append(utils.get_normed_data(path))
    
    return list_data

def save_data(data):

    count_reg = utils.get_count_reg(data)
    utils.save_in_db(count_reg, 'registros')

    info_cines = utils.get_info_cines(data)
    utils.save_in_db(info_cines, 'info_cines')
    
    final_data = utils.get_data(data)
    utils.save_in_db(final_data, 'data')

if __name__ == '__main__':
    logging.config.fileConfig('logs.conf')

    list_data = load_data()
    data = pd.concat(list_data)
    save_data(data)
