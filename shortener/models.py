from django.db import models
from .utils import encrypt_id, base62_encode

class URLMapping(models.Model):
    long_url = models.URLField(max_length=2000, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        short_code = base62_encode(encrypt_id(self.pk))
        return f"{short_code} -> {self.long_url[:50]}"

