from django.test import TestCase, Client
from django.urls import reverse
from .models import URLMapping
from .utils import encrypt_id, base62_encode

class URLDeduplicationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = "https://www.google.com"

    def test_duplicate_url_reuses_id(self):
        # First submission
        response1 = self.client.post(reverse('index'), {'longurl': self.url})
        self.assertEqual(URLMapping.objects.count(), 1)
        obj1 = URLMapping.objects.get(long_url=self.url)
        
        # Second submission of same URL
        response2 = self.client.post(reverse('index'), {'longurl': self.url})
        self.assertEqual(URLMapping.objects.count(), 1) # Count should still be 1
        obj2 = URLMapping.objects.get(long_url=self.url)
        
        self.assertEqual(obj1.id, obj2.id)
        
        # Verify both responses show the same short URL
        short_code = base62_encode(encrypt_id(obj1.id))
        self.assertIn(short_code, response1.content.decode())
        self.assertIn(short_code, response2.content.decode())

    def test_api_deduplication(self):
        api_url = reverse('api-shorten')
        
        # First API call
        response1 = self.client.post(api_url, {'long_url': self.url}, content_type='application/json')
        self.assertEqual(response1.status_code, 201)
        id1 = response1.data['id']
        
        # Second API call
        response2 = self.client.post(api_url, {'long_url': self.url}, content_type='application/json')
        self.assertEqual(response2.status_code, 201)
        id2 = response2.data['id']
        
        self.assertEqual(id1, id2)
        self.assertEqual(URLMapping.objects.count(), 1)
