from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import URLMapping
from .serializers import URLMappingSerializer
from .utils import decrypt_id, base62_decode ,encrypt_id, base62_encode

class URLCreateAPIView(generics.CreateAPIView):
    queryset = URLMapping.objects.all()
    serializer_class = URLMappingSerializer

def index(request):
    context = {}
    if request.method == "POST":
        long_url = request.POST.get("longurl")
        if long_url:
            obj, created = URLMapping.objects.get_or_create(long_url=long_url)
            short_code = base62_encode(encrypt_id(obj.pk))
            
            short_url = request.build_absolute_uri('/') + short_code
            context['short_url'] = short_url
            
    return render(request, 'index.html', context)

def redirect_view(request, short_code):
    scrambled_id = base62_decode(short_code)

    original_id = decrypt_id(scrambled_id)

    mapping = get_object_or_404(URLMapping, id=original_id)
    
    return redirect(mapping.long_url)
