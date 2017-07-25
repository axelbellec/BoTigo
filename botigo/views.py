import json

import apiai

from flask import jsonify, request, make_response

from botigo import app, NAMESPACE
from botigo import config
from botigo import tracing


log = tracing.tracer(NAMESPACE)
ai = apiai.ApiAI(config.API_AI_CLIENT_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'ping': 'pong'}), 200


@app.route('/apiai', methods=['POST'])
def webhook_apiai():
    req = request.get_json(silent=True, force=True)

    log.info('receiving apiai request', request=req)

    res = json.dumps(processRequest(req))

    log.info('processing apiai request', res=res)

    response = make_response(res)

    log.info('making apiai response', response=response)

    return response


def processRequest(request):
    if request.get("result").get("action") != "findNearestStops":
        return {}

    last_context = request['result']['contexts'][-1]
    response = {}

    return response
