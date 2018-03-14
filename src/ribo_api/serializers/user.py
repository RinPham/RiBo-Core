from rest_framework_mongoengine.serializers import DocumentSerializer

from ribo_api.models.user import User


class UserSerializer(DocumentSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        obj = User.objects.create(**validated_data)
        return obj
