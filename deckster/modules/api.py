import logging
import json
import deckster.common.configs as cfg
from deckster.common.core import deck_vault, reload
from deckster.common.scheduler import clear_jobs
from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify

app = Flask("Deckster API")

logger = logging.getLogger("deckster")
logger.debug("API module loaded.")
api_port = cfg.read_config("api_port")

if api_port == None:
    api_port = 5000

@app.route('/deck/reload')
def reload_deck():
    try:
        clear_jobs()
        reload(deck_vault.deck)
    except Exception as e:
        ret = jsonify(f"Could not reload deck: {e}")
        logger.error(f"Could not reload deck: {e}")
        ret.status_code = 500
        return ret
    return jsonify("Deck reloaded")

http_server = WSGIServer(('', api_port), app, log=logger, error_log=logger)
http_server.serve_forever().start()