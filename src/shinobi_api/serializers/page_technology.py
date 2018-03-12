from shinobi_api.models import PageTechnology
from rest_framework_mongoengine.serializers import DocumentSerializer

class PageTechnologySerializer(DocumentSerializer):
    class Meta:
        model = PageTechnology
        fields = '__all__'
