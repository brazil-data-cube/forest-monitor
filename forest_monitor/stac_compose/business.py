import json

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
    def search_kepler_stac(cls, url, collection, bbox, time=False):
        params = {
            'bbox': bbox,
            'limit': 100,
            'collections': [collection.upper()]
        }
        if time:
            params['datetime'] = time

        response = StacComposeServices.search_items(url, params)
        if not response:
            return []
        # retornar somente parametros L4
        features = response['features'] if response.get('features') else [response]
        listL4 = []
        pattern = "L4"
        for i in features:

            if i.get('id') and pattern in i['id']:
                listL4.append(i)

        return listL4

    @classmethod
    def search_element84(cls, url, collection, bbox, time=False, limit=100):

        data = {
            'collections': [collection],
            'intersects': {
                "type": "Polygon",
                "coordinates": json.loads(bbox)
            }
        }

        if time:
            # range temporal
            data['datetime'] = time
        if limit:
            # limit
            data['limit'] = limit if int(limit) <= 100 else 100

        response = StacComposeServices.search_items_post_element84(url, data)
        if not response:
            return []

        result_features = []
        # get all features
        if int(limit) <= 100 or int(response['meta']['found']) <= 100:
            result_features += response['features']

        # get 1000 features at a time
        else:
            qnt_all_features = response['meta']['found']
            for x in range(0, int(qnt_all_features / 100) + 1):
                data['page'] = x + 1
                response_by_page = StacComposeServices.search_items_post_element84(url, data)
                if response_by_page:
                    result_features += response_by_page['features']

        return result_features

    @classmethod
    def search_usgs(cls, url, collection, bbox, time=False, limit=100):

        data = {
            'collections': [collection],
            'intersects': {
                "type": "Polygon",
                "coordinates": json.loads(bbox)
            },
            # 'properties': {
            #     "platform": "LANDSAT_8"
            # }
        }

        if time:
            # range temporal
            data['datetime'] = time
        if limit:
            # limit
            data['limit'] = limit if int(limit) <= 100 else 100

        response = StacComposeServices.search_items_post_usgs(url, data)
        #print(bbox + " \n")

        if not response:
            return []

        result_features = []
        # get all features
        if int(limit) <= 100 or int(response['meta']['found']) <= 100:
            result_features += response['features']

        # get 1000 features at a time
        else:
            qnt_all_features = response['meta']['found']
            for x in range(0, int(qnt_all_features / 100) + 1):
                data['page'] = x + 1
                response_by_page = StacComposeServices.search_items_post_usgs(url, data)
                if response_by_page:
                    result_features += response_by_page['features']
        
        return result_features
    
    @classmethod
    def search(cls, collections, bbox, polygon, time=False, limit=100):

        result_features = []
        for collection in collections.split(','):
            if 'CBERS' in collection:
                result_features += cls.search_kepler_stac(cls.get_providers()['KEPLER_STAC'],
                                                          collection, bbox, time)

            elif 'sentinel' in collection:
                result_features += cls.search_element84(cls.get_providers()['ELEMENT84'],
                                                        collection, polygon, time, limit)

            # elif 'landsat' in collection:
            #     result_features += cls.search_element84(cls.get_providers()['ELEMENT84'],
            #                                             collection, polygon, time, limit)

            elif 'landsat-c2l2-sr' in collection:
                result_features += cls.search_usgs(cls.get_providers()['USGS'],
                                                        collection, polygon, time, limit)

        return result_features
