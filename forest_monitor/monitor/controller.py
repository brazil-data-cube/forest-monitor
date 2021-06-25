import json

from bdc_core.decorators.auth import require_oauth_scopes
from bdc_core.utils.flask import APIResource
from flask import request

from forest_monitor.config import APPNAME
from forest_monitor.monitor import ns
from forest_monitor.monitor.business import FeatureBusiness

api = ns


@api.route('/add')
class FeatureCreationController(APIResource):
    @require_oauth_scopes(scope="{}:manage:POST".format(APPNAME))
    def post(self):
        """
        Add a feature to the database
        """
        FeatureBusiness.add(request.get_json(), user_id=request.user_id)

        return {"status": 201}, 201


@api.route('/get/<string:feature_id>')
class FeatureGetController(APIResource):
    @require_oauth_scopes(scope="{}:manage:POST".format(APPNAME))
    def get(self, feature_id):
        feature = FeatureBusiness.get(feature_id)
        response = json.dumps(feature, indent=2)

        return response


@api.route('/update/<string:feature_id>')
class FeatureUpdateController(APIResource):
    @require_oauth_scopes(scope="{}:manage:POST".format(APPNAME))
    def post(self, feature_id):
        FeatureBusiness.update(request.get_json(), feature_id)

        return {"status": 200}, 200


@api.route('/split/<string:feature_id>')
class FeatureCreationController(APIResource):
    @require_oauth_scopes(scope="{}:manage:POST".format(APPNAME))
    def post(self, feature_id):
        params = request.get_json()

        FeatureBusiness.updateGeom(params, feature_id)

        FeatureBusiness.add(params, user_id=request.user_id)

        return {"status": 201}, 201


@api.route('/delete/<string:feature_id>')
class FeatureDeleteController(APIResource):
    @require_oauth_scopes(scope="{}:manage:DELETE".format(APPNAME))
    def delete(self, feature_id):
        FeatureBusiness.delete(feature_id)

        return {"status": 204}, 204
