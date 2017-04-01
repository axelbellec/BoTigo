import json

import apiai
import datetime as dt
import googlemaps

from flask import jsonify, request, make_response

from botigo import app
from botigo.bot import Bot
from botigo import config
from botigo import tracing
from botigo import NAMESPACE

FB_VERIFY_TOKEN = config.FB_VERIFY_TOKEN

bot = Bot(config.FB_ACCESS_TOKEN)

log = tracing.tracer(NAMESPACE)

gmaps = googlemaps.Client(key=config.GOOGLE_MAPS_GEOCODING_API)

ai = apiai.ApiAI(config.API_AI_CLIENT_ACCESS_TOKEN)


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'ping': 'pong'}), 200


@app.route('/', methods=['GET'])
def verify():
    # When the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if not request.args.get('hub.verify_token') == FB_VERIFY_TOKEN:
            log.error('verification token mismatch')
            return 'Verification token mismatch', 403
        return request.args['hub.challenge'], 200
    log.info('valid authentification')
    return 'Valid authentification', 200


@app.route('/', methods=['POST'])
def webhook():

    # Processing incoming messaging events
    data = request.get_json()
    log.debug('incoming messaging events', data=data)

    if data['object'] == 'page':

        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                # The facebook ID of the person sending you the message
                sender_id = messaging_event['sender']['id']

                if messaging_event.get('read'):
                    log.debug('message read', sender_id=sender_id)
                elif messaging_event.get('delivery'):
                    log.debug('message delivered', sender_id=sender_id)
                elif messaging_event.get('message'):

                    # Someone sent us his location
                    if bot.has_location_payload(messaging_event):
                        coordinates = bot.get_location_payload(messaging_event)
                        log.info('coordinates', coordinates=coordinates)

                        bot.send_fb_msg(sender_id, 'Vos coordonnées : (lat={lat}, lon={lon})'.format(
                            lat=coordinates['lat'], lon=coordinates['long']))
                        reverse_latlon = gmaps.reverse_geocode((coordinates['lat'], coordinates['long']))
                        user_address = reverse_latlon[0]['formatted_address']
                        bot.send_fb_msg(sender_id, user_address)

                    if bot.has_quick_reply(messaging_event):
                        quick_reply_text = bot.get_quick_reply(messaging_event)
                        bot.send_fb_msg(sender_id, quick_reply_text)
                        log.debug('quick reply', quick_reply=quick_reply_text)

                    # Someone sent us a message
                    if not bot.has_location_payload(messaging_event) and not bot.has_quick_reply(messaging_event):

                        if bot.has_sticker_payload(messaging_event):
                            log.info('user sent a sticker')
                            continue

                        # The recipient's ID, which should be our page's facebook ID
                        _ = messaging_event['recipient']['id']
                        # The message's text
                        message_text = messaging_event['message']['text']
                        log.info('message received', sender_id=sender_id, message=message_text)
                        bot.send_fb_msg(sender_id, message_text)

                # Delivery confirmation
                if messaging_event.get('delivery'):
                    pass

                # Optin confirmation
                if messaging_event.get('optin'):
                    pass

                # User clicked 'postback' button in earlier message
                if messaging_event.get('postback'):
                    pass

    return 'ok', 200


@app.route('/apiai', methods=['POST'])
def webhook_apiai():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)
    print(res)
    res = json.dumps(res, indent=4)
    # print(res)
    response = make_response(res)
    response.headers['Content-Type'] = 'application/json'
    return response


def processRequest(req):
    if req.get("result").get("action") != "findNearestStops":
        return {}
    address = req['result']['contexts'][0]['parameters']['address']
    kind_transport = req['result']['contexts'][0]['parameters']['kindTransport']
    res = findNearestStops(address=address, kind_transport=kind_transport)
    # print(res)
    return {'action': 'done'}, 200


def findNearestStops(address, kind_transport):
    arrival = address + 'Bordeaux'
    geocode_result = gmaps.geocode(arrival)
    location = geocode_result[0]['geometry']['location']
    now = dt.datetime.now()
    directions = gmaps.directions(
        origin='206 Bd du Président Franklin Roosevelt',
        destination=arrival,
        mode='transit',
        transit_mode=kind_transport,
        departure_time=now
    )
    print(directions)
    return geocode_result
