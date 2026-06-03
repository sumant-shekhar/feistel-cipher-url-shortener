from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from .models import URLMapping
from .serializers import URLMappingSerializer
from .utils import decrypt_id, base62_decode

class URLCreateAPIView(generics.CreateAPIView):
    queryset = URLMapping.objects.all()
    serializer_class = URLMappingSerializer

def redirect_view(request, short_code):
    scrambled_id = base62_decode(short_code)

    original_id = decrypt_id(scrambled_id)

    mapping = get_object_or_404(URLMapping, id=original_id)
    
    return redirect(mapping.long_url)
