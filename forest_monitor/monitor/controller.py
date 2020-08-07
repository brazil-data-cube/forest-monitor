import os
import json
from flask import request
from werkzeug.exceptions import InternalServerError, BadRequest
from bdc_core.utils.flask import APIResource
from forest_monitor.monitor import ns
from forest_monitor.monitor.business import FeatureBusiness
from bdc_core.decorators.auth import require_oauth_scopes
from forest_monitor.config import APPNAME

api = ns

@api.route('/')
class FeatureCreationController(APIResource):
    @require_oauth_scopes(scope="{}:manage:POST".format(APPNAME))
    def post(self):
        """
        Add a feature to the database
        """
        FeatureBusiness.add(request.get_json(), user_id=request.user_id)

        return {"status": 201}, 201

@api.route('/<string:feature_id>')
class FeatureController(APIResource):
    @require_oauth_scopes(scope="{}:manage:POST".format(APPNAME))
    def get(self, feature_id):
        FeatureBusiness.get(feature_id)
        
        return {"status": 200}, 200

@api.route('/update/<string:feature_id>')
class FeatureController(APIResource):
    @require_oauth_scopes(scope="{}:manage:POST".format(APPNAME))
    def get(self, feature_id):
        FeatureBusiness.put(feature_id)
        
        return {"status": 200}, 200




@api.route('/<string:feature_id>')
class FeatureController(APIResource):
    @require_oauth_scopes(scope="{}:manage:DELETE".format(APPNAME))
    def delete(self, feature_id):
        FeatureBusiness.delete(feature_id)

        return {"status": 204}, 204

