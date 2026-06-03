from django.test import TestCase, Client
from django.urls import reverse
from .models import URLMapping
from .utils import encrypt_id, decrypt_id, base62_encode, base62_decode

class URLShortenerTests(TestCase):

    def test_utils_consistency(self):
        """
        Tests that encrypting and then decrypting an ID returns the original ID,
        and Base62 encoding/decoding is consistent.
        """
        original_pks = [1, 100, 5000, 99999]
        for pk in original_pks:
            scrambled = encrypt_id(pk)
            encoded = base62_encode(scrambled)
            
            # Decode and Decrypt
            decoded_scrambled = base62_decode(encoded)
            decrypted_pk = decrypt_id(decoded_scrambled)
            
            self.assertEqual(pk, decrypted_pk)
            self.assertTrue(len(encoded) <= 7)

    def test_index_view_creation(self):
        """
        Tests creating a short URL via the web form.
        """
        response = self.client.post(reverse('index'), {'longurl': 'https://www.google.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('short_url', response.context)
        self.assertTrue(URLMapping.objects.filter(long_url='https://www.google.com').exists())

    def test_api_creation(self):
        """
        Tests creating a short URL via the DRF API.
        """
        response = self.client.post(reverse('api-shorten'), {'long_url': 'https://github.com'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('short_url', response.data)

    def test_redirection(self):
        """
        Tests that accessing a short URL redirects to the correct long URL.
        """
        # 1. Create a mapping
        long_url = 'https://python.org'
        obj = URLMapping.objects.create(long_url=long_url)
        
        # 2. Generate the short code
        short_code = base62_encode(encrypt_id(obj.id))
        
        # 3. Attempt redirection
        response = self.client.get(reverse('redirect', kwargs={'short_code': short_code}))
        self.assertRedirects(response, long_url, fetch_redirect_response=False)
