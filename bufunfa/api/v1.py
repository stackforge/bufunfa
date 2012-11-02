# Copyright 2012 Bouvet ASA
#
# Author: Endre Karlson <endre.karlson@bouvet.no>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import datetime

import flask

from bufunfa.openstack.common import log
from bufunfa.central import api as capi

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
    app = flask.Flask('bufunfa.api.v1')
    app.register_blueprint(blueprint)
    return app
