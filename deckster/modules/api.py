import logging
import json
import deckster.common.configs as cfg
from deckster.common.core import deck_vault, reload
from deckster.common.scheduler import clear_jobs
from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify, request, make_response
from deckster.plugins.builtins.lock import lock, unlock, blank_lock

app = Flask("Deckster API")

logger = logging.getLogger("deckster")
logger.debug("API module loaded.")
api_port = cfg.read_config("api_port")
api_token = cfg.read_config("api_token")

if api_port == None:
    api_port = 5000

def require_token(f):
    def decorator(*args, **kwargs):
        if api_token == None:
                logger.error("No token was set, cannot complete request.")
                return make_response(jsonify(operation="failed", message="No token defined by the server. Contact the administrator."), 500)
        if api_token == "disabled":
            logger.info("Authentication is disabled")
            return f(*args, **kwargs)            
        if 'token' in request.headers:
            token = request.headers['token']
            if token != api_token:
                return make_response(jsonify(operation="failed", message="Invalid token."), 403)
        else:
            return make_response(jsonify(operation="failed", message="Missing token."), 401)
        logger.info("Auth success.")
        return f(*args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator

@app.route('/deck/reload', methods=['POST'])
@require_token
def reload_deck():
    try:
        clear_jobs()
        reload(deck_vault.deck)
    except Exception as e:
        return make_response(jsonify(operation="failed", message=f"Could not reload deck: {e}"), 500)
    return make_response(jsonify(operation="success", message="Deck reloaded"), 200)

@app.route('/deck/lock', methods=['POST'])
@require_token
def lock_deck():
    try:
        data = request.get_json()
        logger.debug("Request parsed")
        if "mode" in data:
            if data["mode"] == "keyed":
                combination = data["combination"]
                key_on_lock = data["icon_key"]
                icon = data["icon"]
                lock(deck_vault.deck, combination, key_on_lock, icon)
            elif data["mode"] == "blank":
                blank_lock(deck_vault.deck)
        else:
            return make_response(jsonify(operation="failed", message=f"No mode was specified."), 400)
    except Exception as e:
        return make_response(jsonify(operation="failed", message=f"Could not lock deck: {e}"), 500)
    return make_response(jsonify(operation="success", message="Deck locked"), 200)

@app.route('/deck/unlock', methods=['POST'])
@require_token
def unlock_deck():
    try:
        unlock(deck_vault.deck)
    except Exception as e:
        return make_response(jsonify(operation="failed", message=f"Could not unlock deck: {e}"), 500)
    return make_response(jsonify(operation="success", message="Deck unlocked"), 200)

http_server = WSGIServer(('', api_port), app, log=logger, error_log=logger)
http_server.serve_forever().start()