import re
import json
import logging
from email.message import Message

from channels import Group
from channels.sessions import channel_session
from ribo_api.models import Channel
from ribo_api.serializers.message import MessageSerializer
from ribo_api.services.conversation import ConversationService

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
            log.debug('invalid ws path=%s', message['path'])
            return
        channel = Channel.objects(user_id=user_id)
        if not channel:
            channel = Channel(user_id=user_id)
            channel.save()
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
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
        log.debug('no room in channel_session')
        return
    except Channel.DoesNotExist:
        log.debug('recieved message, but channel does not exist')
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message.content['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return

    if set(data.keys()) != set(('user_id', 'body')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        # log.debug('chat message room=%s handle=%s message=%s',
        #     channel.user_id, data['handle'], data['message'])
        m = ConversationService.reply(data)

        # See above for the note about Group
        Group('chat-'+user_id, channel_layer=message.channel_layer).send({'message': MessageSerializer(m,many=True).data})

@channel_session
def ws_disconnect(message):
    try:
        user_id = message.channel_session['channel']
        channel = Channel.objects.get(user_id=user_id)
        Group('chat-'+user_id, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, channel.DoesNotExist):
        pass
