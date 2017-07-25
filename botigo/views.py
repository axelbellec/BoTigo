import json

import apiai

from flask import jsonify, request, make_response

from botigo import app, NAMESPACE
from botigo import config
from botigo import tracing
from botigo.messaging import FacebookSimpleMessage, BasicMessage
from botigo.utils import to_ascii_chars, get_last_departures_times
from botigo import mocks

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

    # Contexts list may be empty
    contexts = request['result'].get('contexts', None)
    last_context = contexts[-1] if contexts else None
    log.info('last context', context=last_context)

    if request['result'].get('action') == 'search_next_departures':
        stop = to_ascii_chars(last_context.get('parameters', {}).get('stop', '')).lower()
        direction = to_ascii_chars(last_context.get('parameters', {}).get('direction', '')).lower()

        if stop and direction:
            log.info('finding next departure times', stop=stop, direction=direction)

            if stop == 'barriere saint-genes' and direction in ['berges de la garonne', 'la cite du vin']:
                url = mocks.URLS['tram']['Ligne B'][
                    'BORDEAUX Berges de la Garonne / BORDEAUX La Cité du Vin']['TALENCE Barrière Saint-Genès']

            elif stop == 'barriere saint-genes' and direction in ['pessac centre', 'france alouette']:
                url = mocks.URLS['tram']['Ligne B'][
                    'PESSAC Centre / PESSAC France Alouette']['TALENCE Barrière Saint-Genès']

            elif stop == 'la cite du vin' and direction in ['berges de la garonne', 'la cite du vin']:
                url = mocks.URLS['tram']['Ligne B'][
                    'BORDEAUX Berges de la Garonne / BORDEAUX La Cité du Vin']['BORDEAUX La Cité du Vin']

            elif stop == 'la cite du vin' and direction in ['pessac centre', 'france alouette']:
                url = mocks.URLS['tram']['Ligne B'][
                    'PESSAC Centre / PESSAC France Alouette']['BORDEAUX La Cité du Vin']

            else:
                log.warn('stop or direction is unknown')
                return {}

            departure_times = get_last_departures_times(url)

            log.info('sending next departure times', stop=stop, direction=direction, url=url)

            msg = 'Arrêt "{s}" (direction {d})\n{t}'.format(s=stop, d=d, t='\n'.join(departure_times))
            return {
                'messages': [
                    BasicMessage(msg=msg).payload,
                    FacebookSimpleMessage(msg=msg).payload
                ]
            }

    response = {}

    return response
