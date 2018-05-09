from django.conf import settings
import apiai, json
from ribo_api.services.base import BaseService
import os
import requests

API_AI_HOST = os.getenv('API_AI_URL', 'https://api.dialogflow.com/v1/')
API_AI_VERSION = os.getenv('API_AI_VERSION', '20150910')
DEFAULT_TIMEOUT = 10.0


class ApiAiError(Exception):
    pass


def req(access_token, meth, path, params, **kwargs):
    full_url = API_AI_HOST + path + '?v='+API_AI_VERSION
    headers = {
        'authorization': 'Bearer ' + access_token,
        'content-type': 'application/json'
    }
    headers.update(kwargs.pop('headers', {}))
    rsp = requests.request(
        meth,
        full_url,
        headers=headers,
        params=params,
        timeout=DEFAULT_TIMEOUT,
        **kwargs
    )
    if rsp.status_code > 200:
        raise ApiAiError('Dialogflow responded with status: ' + str(rsp.status_code) +
                       ' (' + rsp.reason + ')')
    json = rsp.json()
    if 'error' in json:
        raise ApiAiError('Dialogflow responded with an error: ' + json['error'])

    return json

class DialogFlow(object):

    access_token = None
    ai = None

    def __init__(self):
        self.access_token = settings.APIAI_CLIENT_ACCESS_TOKEN
        self.ai = apiai.ApiAI(self.access_token)

    def get_query(self, query=None, language='en', user_id=None):
        if query:
            self.request = self.ai.text_request()
            self.request.lang = language
            self.request.session_id = user_id
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
    def get_result(cls, user_id, text, **kwargs):
        ai = DialogFlow()
        response = ai.get_query(text, user_id=user_id)
        return response['result']

    @classmethod
    def get_response(cls, user_id, text, **kwargs):
        ai = DialogFlow()
        response = ai.get_query(text, user_id=user_id)
        return response

    @classmethod
    def del_contents(cls, user_id, **kwargs):
        res = req(settings.APIAI_CLIENT_ACCESS_TOKEN, 'delete', 'contexts', {'sessionId':user_id})
        return res



