from flask import jsonify, request
import googlemaps
import datetime as dt

from wit import Wit

from botigo import app
from botigo.bot import Bot
from botigo import config
from botigo import tracing
from botigo import NAMESPACE

FB_VERIFY_TOKEN = config.FB_VERIFY_TOKEN

bot = Bot(config.FB_ACCESS_TOKEN)

log = tracing.tracer(NAMESPACE)

gmaps = googlemaps.Client(key=config.GOOGLE_MAPS_GEOCODING_API)


def send(request, response):
    """ WIT AI sender function. """
    session_id = request['session_id']
    text = response['text'].decode('utf-8')
    print(request['context'])
    if response.get('quickreplies'):
        bot.send_quick_reply(session_id, text, response['quickreplies'])
    else:
        bot.send_fb_msg(session_id, text)


def merge(request):
    context = request['context']
    entities = request['entities']

    kind_action = first_entity_value(entities, 'kind_action')
    if kind_action:
        context['kind_action'] = kind_action
    destination = first_entity_value(entities, 'destination')
    if destination:
        context['destination'] = destination
    date_depart = first_entity_value(entities, 'date-depart')
    if date_depart:
        context['date-depart'] = date_depart
    travel_mode = first_entity_value(entities, 'TravelMode')
    if travel_mode:
        context['TravelMode'] = travel_mode
    return context


def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def get_directions(request):
    context = request['context']
    destination = context['destination']
    travel_mode = context['TravelMode']
    date = dt.datetime.now()
    directions_result = gmaps.directions('Cdiscount, Bordeaux',
                                         destination,
                                         mode='transit',
                                         transit_mode=travel_mode,
                                         departure_time=now,
                                         language='fr')
    print(directions_result)


actions = {
    'send': send,
    'merge': merge,
    'get_directions': get_directions
}

WitAI = Wit(access_token=config.WIT_AI_CLIENT_ACCESS_TOKEN, actions=actions)


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
    log.info('incoming messaging events', data=data)

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
                        # bot.send_fb_msg(sender_id, quick_reply_text)
                        WitAI.run_actions(session_id=sender_id, message=quick_reply_text)

                    # Someone sent us a message
                    if not bot.has_location_payload(messaging_event) and not bot.has_quick_reply(messaging_event):

                        if bot.has_sticker_payload(messaging_event):
                            log.info('user sent a sticker')
                            continue

                        # The recipient's ID, which should be our page's facebook ID
                        _ = messaging_event['recipient']['id']
                        # The message's text
                        message_text = messaging_event['message']['text']

                        # # if message_text.lower() == 'kind':
                        # #     bot.send_kind_msg(sender_id, msg='Quel type de transport voulez-vous prendre ?')
                        # # elif message_text.lower() == 'moment':
                        # #     bot.send_moment_msg(sender_id, msg='Dans combien de temps voulez-vous partir ?')
                        # # else:
                        #     # bot.send_fb_msg(sender_id, message_text)
                        WitAI.run_actions(session_id=sender_id, message=message_text)

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
