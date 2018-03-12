from shinobi_api.models import Page, Event, Element
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

class PageSerializer(DocumentSerializer):
    class Meta:
        model = Page
        fields = '__all__'

class ElementSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Element
        fields = '__all__'

class EventSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Event
        fields = '__all__'