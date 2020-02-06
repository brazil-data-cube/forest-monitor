from flask import Blueprint
from flask_restplus import Api
from forest_monitor.monitor.controller import api as monitor_ns
from forest_monitor.stac_compose.controller import api as stac_compose_ns


blueprint = Blueprint('forest_monitor', __name__, url_prefix='/api')

api = Api(blueprint, doc=False)

api.add_namespace(monitor_ns)
api.add_namespace(stac_compose_ns)