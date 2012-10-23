import datetime

import flask

from billistix.openstack.common import log
from billistix.openstack.common import timeutils

from billistix import storage

LOG = log.getLogger(__name__)

blueprint = flask.Blueprint('v1', __name__)


@blueprint.route("/rates")
def list_rates():
    return flask.request.storage_engine.get_rates()
