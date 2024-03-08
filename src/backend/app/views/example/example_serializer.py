from rest_framework import serializers
from app.models.app_user import AppUserModel

class ExampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUserModel
        fields = '__all__'