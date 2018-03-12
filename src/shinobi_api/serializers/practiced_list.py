from rest_framework_mongoengine.serializers import DocumentSerializer
from shinobi_api.models import PracticedList


class PracticedListSerializer(DocumentSerializer):

    class Meta:
        model = PracticedList