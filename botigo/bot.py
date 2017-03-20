import copy
import os
import json
import requests


from botigo import config


class Bot():

    def __init__(self, access_token, **kwargs):
        """
        @required:
                access_token
        @optional:
                api_version
        """

        self.api_version = kwargs.get('api_version') or config.FB_GRAPH_API_VERSION
        self.graph_url = 'https://graph.facebook.com/v{0}'.format(self.api_version)
        self.graph_msg_url = '{}/me/messages'.format(self.graph_url)
        self.params = {
            'access_token': config.FB_ACCESS_TOKEN
        }
        self.headers = {
            'Content-Type': 'application/json'
        }

    def post_payload(self, data, **kwargs):
        response = requests.post(
            self.graph_msg_url,
            params=self.params,
            headers=self.headers,
            data=data
        )
        if response.status_code != 200:
            return response.json()
        return {}

    def send_fb_msg(self, recipient_id, message_text):
        print('sending message to {recipient}: {text}'.format(
            recipient=recipient_id, text=message_text))

        data = json.dumps({
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': message_text
            }
        })
        self.post_payload(data)

    def send_card_msg(self, recipient_id, elements=[]):

        data = json.dumps({
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'attachment': {
                    'type': 'template',
                    'payload': {
                            'template_type': 'generic',
                            'elements': elements
                    }
                }
            }
        })

        self.post_payload(data)

    def send_location_msg(self, recipient_id, msg):

        data = json.dumps({
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': msg,
                'quick_replies': [
                    {
                        'content_type': 'location',
                    }
                ]
            }
        })

        self.post_payload(data)

    def send_kind_msg(self, recipient_id, msg):

        data = json.dumps({
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': msg,
                'quick_replies': [
                    {
                        'content_type': 'text',
                        'title': 'Prendre un vélo',
                        'payload': 'prendre'
                    },
                    {
                        'content_type': 'text',
                        'title': 'Poser un vélo',
                        'payload': 'déposer'
                    }
                ]
            }
        })

        self.post_payload(data)

    def send_moment_msg(self, recipient_id, msg):

        data = json.dumps({
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': msg,
                'quick_replies': [
                    {
                        'content_type': 'text',
                        'title': 'Maintenant',
                        'payload': 'now'
                    },
                    {
                        'content_type': 'text',
                        'title': 'Dans 10 min.',
                        'payload': '10_minutes'
                    },
                    {
                        'content_type': 'text',
                        'title': 'Dans 30 min.',
                        'payload': '30_minutes'
                    }
                ]
            }
        })
        self.post_payload(data)

    def get_user_fullname(self, recipient_id, fields=['first_name', 'last_name']):
        params = copy.deepcopy(self.params)

        if fields is not None and isinstance(fields, (list, tuple)):
            params['fields'] = ','.join(fields)

        request_endpoint = '{}/{}'.format(self.graph_url, recipient_id)
        res = requests.get(request_endpoint, params=params, headers=self.headers)

        if res.status_code == 200:
            return res.json()
        return None

    def has_location_payload(self, messaging_event):
        try:
            _ = messaging_event['message']['attachments'][0]['payload']['coordinates']
            return True
        except:
            return False

    def has_sticker_payload(self, messaging_event):
        try:
            _ = messaging_event['message']['attachments'][0]['payload']['sticker_id']
            return True
        except:
            return False

    def get_location_payload(self, messaging_event):
        return messaging_event['message']['attachments'][0]['payload']['coordinates']

    def has_quick_reply(self, messaging_event):
        try:
            _ = messaging_event['message']['quick_reply']
            return True
        except:
            return False

    def get_quick_reply(self, messaging_event):
        return messaging_event['message']['text']
