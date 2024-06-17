from rest_framework import serializers
from app.models import FrontMenuModel

class FrontMenuSerializer(serializers.ModelSerializer):
    item_key = serializers.CharField(max_length=25, required=True)
    item_title = serializers.CharField(max_length=100, required=True)
    item_url = serializers.CharField(max_length=100, required=True)
    father_menu_id = serializers.IntegerField(default=None, required=False)
    sort_seq = serializers.IntegerField(default=0)
    is_active = serializers.BooleanField(default=True)
    item_description = serializers.CharField(default=None, max_length=2000, required=False)

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if attrs['father_menu_id'] is not None:
            exists = FrontMenuModel.objects.filter(pk=attrs['father_menu_id']).count()
            if exists != 1:
                raise serializers.ValidationError('Father menu not exists')
        exists_url = FrontMenuModel.objects.filter(item_url=attrs['item_url']).count()
        if exists_url != 0:
            raise serializers.ValidationError('this front path already exists')
        return validated_data
    class Meta:
        model = FrontMenuModel
        fields = '__all__'