from datetime import datetime
from json import JSONEncoder

from cerberus import Validator


def validate_date(s):
    dates = s.split("/")
    for date in dates:
        if date.split('T')[0] and not datetime.strptime(date.split('T')[0], '%Y-%m-%d'):
            return None
    return s


def validate_collections(collections):
    for c in collections.split(','):
        if c not in ["CBERS4A-MUX", "CBERS4A-AWFI", "CBERS4-MUX", "CBERS4-AWFI", "sentinel-s2-l2a-cogs", "landsat-c2l2-sr"]: # "landsat-8-l1-c1"
            return None
    return collections.split(',')


def validate_bbox(box):
    list_bbox = box.split(',')
    coordinates = [float(b) for b in list_bbox]
    return coordinates if len(coordinates) == 4 else None


def validate_cloud(cloud):
    return float(cloud) if 0 < float(cloud) <= 100 else None


def validate_limit(limit):
    return int(limit) if float(limit) > 0 else None


def search():
    base = {
        'collections': {"type": "list", "coerce": validate_collections, "empty": False, "required": True},
        'bbox': {"type": "list", "coerce": validate_bbox, "empty": False, "required": True},
        'polygon': {"type": "string", "empty": True, "required": False},
        'cloud_cover': {"type": "number", "coerce": validate_cloud, "empty": True, "required": False},
        'time': {"type": "string", "coerce": validate_date, "empty": True, "required": False},
        'limit': {"type": "number", "coerce": validate_limit, "empty": True, "required": False}
    }
    return base


def validate(data, type_schema):
    schema = eval('{}()'.format(type_schema))

    v = Validator(schema)
    if not v.validate(data):
        return v.errors, False
    return data, True


class JSONEnc(JSONEncoder):
    def default(self, o):
        return o._asdict()
