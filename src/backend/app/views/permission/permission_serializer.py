from rest_framework import serializers
from app.models.app_user import AppUserModel

class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppUserModel
        fields = '__all__'