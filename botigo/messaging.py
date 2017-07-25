class SimpleMessage(object):

    def __init__(self, msg):
        self.msg = msg

    @property
    def payload(self):
        raise NotImplementedError


class BasicMessage(SimpleMessage):

    def __init__(self, msg):
        super(BasicMessage, self).__init__(
            msg=msg
        )

    @property
    def payload(self):
        return {
            'type': 0,
            'speech': self.msg
        }


class FacebookSimpleMessage(SimpleMessage):

    def __init__(self, msg):
        super(FacebookSimpleMessage, self).__init__(
            msg=msg
        )

    @property
    def payload(self):
        return {
            'type': 0,
            'platform': 'facebook',
            'speech': self.msg
        }
