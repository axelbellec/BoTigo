import copy
import json
import requests

from botigo import config
from botigo import NAMESPACE
from botigo import tracing


log = tracing.tracer(NAMESPACE)


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

        log.info('sending message', recipient=recipient_id, text=message_text)

        data = json.dumps({
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': message_text
            }
        })
        self.post_payload(data)

    def send_card_msg(self, recipient_id, elements):

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
                        'title': 'Tram \ud83d\ude8b',
                        'payload': 'tram'
                    },
                    {
                        'content_type': 'text',
                        'title': 'Bus \ud83d\ude8c',
                        'payload': 'bus'
                    },
                    {
                        'content_type': 'text',
                        'title': 'Vélo \ud83d\udeb2',
                        'payload': 'velo'
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

    def get_user_fullname(self, recipient_id):
        params = copy.deepcopy(self.params)
        params['fields'] = ','.join(['first_name', 'last_name'])

        request_endpoint = '{}/{}'.format(self.graph_url, recipient_id)
        res = requests.get(request_endpoint, params=params, headers=self.headers)

        if res.status_code == 200:
            return res.json()
        return None

    @classmethod
    def has_location_payload(cls, messaging_event):
        try:
            _ = messaging_event['message']['attachments'][0]['payload']['coordinates']
        except KeyError:
            log.error('KeyError: Unable to access coordinates from message attachments.')
            return False
        except Exception as err:
            log.error('Exception: Unable to access coordinates from message attachments.', err=err)
            return False
        return True

    @classmethod
    def has_sticker_payload(cls, messaging_event):
        try:
            _ = messaging_event['message']['attachments'][0]['payload']['sticker_id']
        except KeyError:
            log.error('KeyError: Unable to access sticker_id from message attachments.')
            return False
        except Exception as err:
            log.error('Exception: Unable to access sticker_id from message attachments.', err=err)
            return False
        return True

    @classmethod
    def get_location_payload(cls, messaging_event):
        return messaging_event['message']['attachments'][0]['payload']['coordinates']

    @classmethod
    def has_quick_reply(cls, messaging_event):
        try:
            _ = messaging_event['message']['quick_reply']
        except KeyError:
            log.error('KeyError: Unable to access quick reply from message.')
            return False
        except Exception as err:
            log.error('Exception: Unable to access quick reply from message.', err=err)
            return False
        return True

    @classmethod
    def get_quick_reply(cls, messaging_event):
        return messaging_event['message']['text']
