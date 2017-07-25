import json

import apiai

from flask import jsonify, request, make_response

from botigo import app, NAMESPACE
from botigo import config
from botigo import tracing
from botigo.messaging import FacebookSimpleMessage, BasicMessage
from botigo.utils import departure_times


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
    last_context = request['result']['contexts'][-1]

    if request['result'].get('action') == 'search_next_departures':
        stop = last_context.get('parameters', {}).get('stop', None)
        direction = last_context.get('parameters', {}).get('direction', None)

        if stop and direction:
            msg = '\n'.join(departure_times)
            return {
                'messages': [
                    BasicMessage(msg=msg).payload,
                    FacebookSimpleMessage(msg=msg).payload
                ]
            }

    response = {}

    return response
