from flask import jsonify, request

# from wit import Wit

from botigo import app
from botigo.bot import Bot
from botigo import config
from botigo import logging
from botigo import NAMESPACE

FB_VERIFY_TOKEN = config.FB_VERIFY_TOKEN

bot = Bot(config.FB_ACCESS_TOKEN)

log = logging.tracer(NAMESPACE)


# TODO: Add actions methods
# actions = {}
# WitAI = Wit(access_token=config.WIT_AI_CLIENT_ACCESS_TOKEN, actions=actions)


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

                if messaging_event.get('message'):
                    # The facebook ID of the person sending you the message
                    sender_id = messaging_event['sender']['id']
                    log.info('sender id', sender_id=sender_id)

                    # Someone sent us his location
                    if bot.has_location_payload(messaging_event):
                        coordinates = bot.get_location_payload(messaging_event)
                        log.info('coordinates', coordinates=coordinates)

                        bot.send_fb_msg(sender_id, 'Vos coordonnées : (lat={lat}, lon={lon})'.format(
                            lat=coordinates['lat'], lon=coordinates['long']))

                    if bot.has_quick_reply(messaging_event):
                        quick_reply_text = bot.get_quick_reply(messaging_event)
                        bot.send_fb_msg(sender_id, quick_reply_text)

                    # Someone sent us a message
                    if not bot.has_location_payload(messaging_event) and not bot.has_quick_reply(messaging_event):

                        if bot.has_sticker_payload(messaging_event):
                            log.info('user sent a sticker')
                            continue

                        # The recipient's ID, which should be our page's facebook ID
                        _ = messaging_event['recipient']['id']
                        # The message's text
                        message_text = messaging_event['message'].get('text')

                        if message_text.lower() == 'kind':
                            bot.send_kind_msg(sender_id, msg='Quel type de transport voulez-vous prendre ?')
                        elif message_text.lower() == 'moment':
                            bot.send_moment_msg(sender_id, msg='Dans combien de temps voulez-vous partir ?')
                        else:
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
