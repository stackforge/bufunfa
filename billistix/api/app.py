import flask

from billistix.openstack.common import cfg
from billistix import storage
from billistix.api import v1

app = flask.Flask("billistix.api")
app.register_blueprint(v1.blueprint, url_prefix="/v1")

storage.register_opts(cfg.CONF)


@app.before_request
def attach_config():
    flask.request.cfg = cfg.CONF
    storage_engine = storage.get_engine(cfg.CONF)
    flask.request.storage_engine = storage_engine
    flask.request.storage_con = storage_engine.get_connection(cfg.CONF)
