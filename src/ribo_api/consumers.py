import re
import json
import logging
from email.message import Message

from channels import Group
from channels.sessions import channel_session
from ribo_api.models import Channel
from ribo_api.serializers.message import MessageSerializer
from ribo_api.services.conversation import ConversationService
from ribo_api.services.utils import Utils

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /chat/{label}/, and finds a Room if the message path is applicable,
    # and if the Room exists. Otherwise, bails (meaning this is a some othersort
    # of websocket). So, this is effectively a version of _get_object_or_404.
    try:
        prefix, user_id = message.content['path'].strip('/').split('/')
        if prefix != 'message':
            Utils.log('invalid ws path=()'.format(message['path']))
            return
        channel = Channel.objects(user_id=user_id)
        if not channel:
            channel = Channel(user_id=user_id)
            channel.save()
    except ValueError:
        Utils.log('invalid ws path={}'.format(message['path']))
        return

    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    Group('chat-'+user_id, channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['channel'] = channel[0]['user_id']

@channel_session
def ws_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        user_id = message.channel_session['channel']
        channel = Channel.objects(user_id=user_id)[0]
    except KeyError:
        Utils.log('no room in channel_session')
        return
    except Channel.DoesNotExist:
        Utils.log('recieved message, but channel does not exist')
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message.content['text'])
        data['object_id'] = '5af2a5f1012a0f6158002137'
    except ValueError:
        Utils.log("ws message isn't json text={}".format(data))
        return

    if set(data.keys()) != set(('user_id', 'body', 'object_id')):
        Utils.log("ws message unexpected format data={}".format(data))
        return

    if data:
        # log.debug('chat message room=%s handle=%s message=%s',
        #     channel.user_id, data['handle'], data['message'])
        m = ConversationService.reply(data)
        for item in m:
            item = MessageSerializer(item).data
            data = {
                "_id": item['id'],
                "created_at": item['created_at'],
                "updated_at": item['updated_at'],
                "user_id": item['user_id'],
                "content": {
                    "answer_text": item['content']['answer_text'],
                    "question_text": item['content']['question_text'],
                    "from_who": item['content']['from_who']
                },
                "action": item['action'],
                "slots": item['slots'],
                "next_question_id": item['next_question_id']
            }
            Group('chat-' + user_id, channel_layer=message.channel_layer).send({'text': json.dumps(data)})


@channel_session
def ws_disconnect(message):
    try:
        user_id = message.channel_session['channel']
        channel = Channel.objects.get(user_id=user_id)
        Group('chat-'+user_id, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, channel.DoesNotExist):
        pass
