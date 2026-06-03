from rest_framework import serializers
from .models import URLMapping
from .utils import encrypt_id, base62_encode

class URLMappingSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = URLMapping
        fields = ['id', 'long_url', 'short_url', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_short_url(self, obj):
        # We scramble the PK using Feistel and then encode in Base62
        scrambled_id = encrypt_id(obj.id)
        short_code = base62_encode(scrambled_id)
        
        # In a real app, we'd use request.build_absolute_uri()
        # but for this simple version, we'll just return the code
        return short_code
