from rest_framework_mongoengine.serializers import DocumentSerializer

from ribo_api.models.api import Api


class ApiSerializer(DocumentSerializer):

    class Meta:
        model = Api
        fields = '__all__'