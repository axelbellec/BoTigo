import json
import os
import pickle

from flask import Blueprint, jsonify, request
import datetime as dt

from botigo import app
from botigo.bot import Bot
from botigo import config
from botigo import logging
from botigo import NAMESPACE

FB_VERIFY_TOKEN = config.FB_VERIFY_TOKEN

bot = Bot(config.FB_ACCESS_TOKEN)

log = logging.tracer(NAMESPACE)


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

                    if bot.has_quick_reply(messaging_event):
                        pass

                    # Someone sent us a message
                    if not bot.has_location_payload(messaging_event) and not bot.has_quick_reply(messaging_event):

                        # The recipient's ID, which should be our page's facebook ID
                        recipient_id = messaging_event['recipient']['id']
                        # The message's text
                        message_text = messaging_event['message'].get('text')

                        bot.send_fb_msg(sender_id, message_text)

                        if bot.has_sticker_payload(messaging_event):
                            log.info('user sent a sticker')

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
