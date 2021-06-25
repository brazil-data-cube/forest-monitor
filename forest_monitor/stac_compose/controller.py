import json

from bdc_core.utils.flask import APIResource
from flask import request
from werkzeug.exceptions import BadRequest

from forest_monitor.stac_compose import ns
from forest_monitor.stac_compose.business import StacComposeBusiness
from forest_monitor.stac_compose.parsers import validate

api = ns

@api.route('/search')
class CollectionsController(APIResource):

    def get(self):
        data, status = validate(request.args.to_dict(flat=True), 'search')
        if status is False:
            raise BadRequest(json.dumps(data))

        """
        Search RF in STAC's
        """
        features = StacComposeBusiness.search(**request.args)

        return {
            "meta": {
                "found": len(features)
            },
            "features": features
        }
