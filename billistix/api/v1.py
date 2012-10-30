import datetime

import flask

from billistix.openstack.common import log
from billistix.central import api as capi

LOG = log.getLogger(__name__)

blueprint = flask.Blueprint('v1', __name__)


@blueprint.route('/rates', methods=['POST'])
def add_rate():
    context = flask.request.environ.get('context')
    values = flask.request.json


@blueprint.route('/rates', methods=['GET'])
def get_rates():
    context = flask.request.environ.get('context')
    print 'CONTEXT', context
    rates = capi.get_rates(context)
    return flask.jsonify(rates=rates)


@blueprint.route('/rates/<rate_id>', methods=['PUT'])
def update_rate(rate_id):
    context = flask.request.environ.get('context')
    values = flask.request.json

    domain = capi.update_rate(context, rate_id)
    return flask.jsonify(domain)


@blueprint.route('/rates/<rate_id>', methods=['DELETE'])
def delete_rate(rate_id):
    context = flask.request.environ.get('context')
    capi.delete_rate(context, rate_id)


def factory(global_config, **local_conf):
    app = flask.Flask('billistix.api.v1')
    app.register_blueprint(blueprint)
    return app
