from rest_framework import serializers
from .models import URLMapping
from .utils import encrypt_id, base62_encode

class URLMappingSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    class Meta:
        model = URLMapping
        fields = ['id', 'long_url', 'short_url', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'long_url': {'validators': []}
        }

    def create(self, validated_data):
        obj, created = URLMapping.objects.get_or_create(**validated_data)
        return obj

    def get_short_url(self, obj):
        scrambled_id = encrypt_id(obj.pk)
        short_code = base62_encode(scrambled_id)
    
        return short_code
