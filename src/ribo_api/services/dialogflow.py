from django.conf import settings
import apiai, json
from ribo_api.services.base import BaseService


class DialogFlow(object):

    access_token = None
    ai = None

    def __init__(self):
        self.access_token = settings.APIAI_CLIENT_ACCESS_TOKEN
        self.ai = apiai.ApiAI(self.access_token)

    def get_query(self, query=None, language='en'):
        if query:
            self.request = self.ai.text_request()
            self.request.lang = language
            self.request.session_id = "<SESSION_ID, UNIQUE FOR EACH USER>"
            self.request.query = query
            response = self.request.getresponse()
            return json.loads(response.read().decode())
        return None


class ApiAIService(BaseService):

    @classmethod
    def get_intents(cls, text, **kwargs):
        ai = DialogFlow()
        response = ai.get_query(text)
        return response['metadata']

    @classmethod
    def get_result(cls, text, **kwargs):
        ai = DialogFlow()
        response = ai.get_query(text)
        return response['result']



