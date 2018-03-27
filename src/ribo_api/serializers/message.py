from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

from ribo_api.models.message import ContentMessage, Message


class ContentMessageSerializer(EmbeddedDocumentSerializer):

    class Meta:
        model = ContentMessage
        fields = '__all__'

class MessageSerializer(DocumentSerializer):

    class Meta:
        model = Message
        fields = '__all__'