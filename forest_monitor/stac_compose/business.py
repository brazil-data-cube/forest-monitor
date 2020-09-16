import json
import os
from pprint import pprint
from forest_monitor.config import BASE_DIR

from forest_monitor.stac_compose.services import StacComposeServices

class StacComposeBusiness():

    @classmethod
    def get_providers(cls):
        with open('{}/stac_compose/static/providers.json'.format(BASE_DIR)) as p:
            data = json.load(p)

        providers = {}
        for key in data.keys():
            providers[key] = data[key]['url']
        return providers

    @classmethod
    def search_development_seed(cls, url, collection, bbox, cloud_cover=False, time=False, limit=100):
        data = {
            'bbox': bbox.split(','),
            'query': {
                'collection': { 'eq': collection }
            }
        }

        if cloud_cover:
            # cloud cover
            data['query']['eo:cloud_cover'] = { "lt": cloud_cover }
        if time:
            # range temporal
            data['time'] = time
        if limit:
            # limit
            data['limit'] = limit if int(limit) <= 1000 else 1000

        response = StacComposeServices.search_items_post(url, data)
        if not response:
            return []

        result_features = []
        # get all features
        if int(limit) <= 1000 or int(response['meta']['found']) <= 1000:
            result_features += response['features']

        # get 1000 features at a time
        else:
            qnt_all_features = response['meta']['found']
            for x in range(0, int(qnt_all_features/1000)+1):
                data['page'] = x+1
                response_by_page = StacComposeServices.search_items_post(url, data)
                if response_by_page:
                    result_features += response_by_page['features']

        return result_features

    @classmethod
    def search_kepler_stac(cls, url, collection, bbox, time=False):
        query = 'bbox={}'.format(bbox)
        query += '&limit={}'.format(300)
        if time:
            # range temporal
            query += '&time={}'.format(time)

        response = StacComposeServices.search_items(url, collection.upper(), query)
        if not response:
            return []
        #retornar somente parametros L4    
        features = response['features'] if response.get('features') else [response] 
        listL4 = []
        padrao = "L4"
        for i in features:

            if i.get('id') and padrao in i['id']:
                #print(i['id'])
                listL4.append(i)
     
        return listL4
        
       

    @classmethod
    def search(cls, collections, bbox, cloud_cover=False, time=False, limit=100):

        result_features = []
        for collection in collections.split(','):
            if 'CBERS' in collection:
                result_features += cls.search_kepler_stac(cls.get_providers()['KEPLER_STAC'],
                                                collection, bbox, time)

            else:
                result_features += cls.search_development_seed(cls.get_providers()['DEVELOPMENT_SEED_STAC'],
                                                collection, bbox, cloud_cover, time, limit)
        return result_features