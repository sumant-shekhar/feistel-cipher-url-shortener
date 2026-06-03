from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics
from .models import URLMapping
from .serializers import URLMappingSerializer
from .utils import decrypt_id, base62_decode

class URLCreateAPIView(generics.CreateAPIView):
    """
    API endpoint to create a shortened URL.
    """
    queryset = URLMapping.objects.all()
    serializer_class = URLMappingSerializer

def index(request):
    """
    Home page view for the URL shortener.
    """
    context = {}
    if request.method == "POST":
        long_url = request.POST.get("longurl")
        if long_url:
            # Create the mapping
            obj = URLMapping.objects.create(long_url=long_url)
            # Use the serializer logic manually or just call the utils
            from .utils import encrypt_id, base62_encode
            short_code = base62_encode(encrypt_id(obj.id))
            
            # Construct absolute URL
            short_url = request.build_absolute_uri('/') + short_code
            context['short_url'] = short_url
            
    return render(request, 'index.html', context)

def redirect_view(request, short_code):
    """
    Decodes the short code and redirects to the long URL.
    """
    # 1. Decode Base62 to get the scrambled ID
    scrambled_id = base62_decode(short_code)
    
    # 2. Decrypt Feistel to get the original Primary Key
    original_id = decrypt_id(scrambled_id)
    
    # 3. Lookup the long URL using the PK
    mapping = get_object_or_404(URLMapping, id=original_id)
    
    return redirect(mapping.long_url)
