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
from bufunfa.central import api as central_api

LOG = log.getLogger(__name__)

blueprint = flask.Blueprint('v1', __name__)


@blueprint.route('/rates', methods=['POST'])
def add_rate():
    context = flask.request.environ.get('context')
    values = flask.request.json

    rate = central_api.add_rate(context, values)
    return flask.jsonify(rate=rate)


@blueprint.route('/rates', methods=['GET'])
def get_rates():
    context = flask.request.environ.get('context')
    rates = central_api.get_rates(context)
    return flask.jsonify(rates=rates)


@blueprint.route('/rates/<rate_id>', methods=['PUT'])
def update_rate(rate_id):
    context = flask.request.environ.get('context')
    values = flask.request.json

    rate = central_api.update_rate(context, rate_id, values)
    return flask.jsonify(rate)


@blueprint.route('/rates/<rate_id>', methods=['DELETE'])
def delete_rate(rate_id):
    context = flask.request.environ.get('context')
    central_api.delete_rate(context, rate_id)


@blueprint.route('/accounts', methods=['POST'])
def add_account():
    context = flask.request.environ.get('context')
    values = flask.request.json

    account = central_api.add_account(context, values)
    return flask.jsonify(account=account)


@blueprint.route('/accounts', methods=['GET'])
def get_accounts():
    context = flask.request.environ.get('context')
    accounts = central_api.get_accounts(context)
    return flask.jsonify(accounts=accounts)


@blueprint.route('/accounts/<account_id>', methods=['PUT'])
def update_account(account_id):
    context = flask.request.environ.get('context')
    values = flask.request.json

    account = central_api.update_account(context, account_id, values)
    return flask.jsonify(account=account)


@blueprint.route('/accounts/<account_id>', methods=['DELETE'])
def delete_account(account_id):
    context = flask.request.environ.get('context')
    central_api.delete_account(context, account_id)


@blueprint.route('/system_accounts', methods=['POST'])
def add_system_account():
    context = flask.request.environ.get('context')
    values = flask.request.json

    account = central_api.add_system_account(context, values)
    return flask.jsonify(system_account=account)


@blueprint.route('/system_accounts', methods=['GET'])
def get_system_accounts():
    context = flask.request.environ.get('context')
    accounts = central_api.get_system_accounts(context)
    return flask.jsonify(system_accounts=accounts)


@blueprint.route('/system_accounts/<account_id>', methods=['PUT'])
def update_system_account(account_id):
    context = flask.request.environ.get('context')
    values = flask.request.json

    account = central_api.update_system_account(context, account_id, values)
    return flask.jsonify(system_account=account)


@blueprint.route('/system_accounts/<account_id>', methods=['DELETE'])
def delete_system_account(account_id):
    context = flask.request.environ.get('context')
    central_api.delete_account(context, account_id)


@blueprint.route('/record', methods=['POST'])
def process_record():
    context = flask.request.environ.get('context')
    values = flask.request.json

    record = central_api.process_record(context, values)
    return flask.jsonify(record)


def factory(global_config, **local_conf):
    app = flask.Flask('bufunfa.api.v1')
    app.register_blueprint(blueprint)
    return app
