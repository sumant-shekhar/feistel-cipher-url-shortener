from django.db import models

class URLMapping(models.Model):
    long_url = models.URLField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} -> {self.long_url[:50]}"
