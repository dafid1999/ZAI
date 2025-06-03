from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from listings.models import Listing, Category
from PIL import Image
import io
import os
from django.conf import settings

class ThumbnailGenerationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        self.category = Category.objects.create(name='TestCat')

        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'username': 'user1', 'password': 'pass'}, format='json')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_thumbnail_created_on_listing_upload(self):
        image_io = io.BytesIO()
        image = Image.new('RGB', (400, 400), 'blue')
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        image_file = SimpleUploadedFile('test.jpg', image_io.read(), content_type='image/jpeg')

        url = reverse('listing-list')
        data = {
            'title': 'Ad with Image',
            'description': 'Desc',
            'price': '9.99',
            'category': 'TestCat',
            'expires_at': '2025-07-01T00:00:00Z',
            'image': image_file
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)

        listing = Listing.objects.first()
        self.assertIsNotNone(listing.thumbnail)

        thumbnail_path = os.path.join(settings.MEDIA_ROOT, listing.thumbnail.name)
        self.assertTrue(os.path.exists(thumbnail_path))

        thumb = Image.open(thumbnail_path)
        self.assertLessEqual(thumb.width, 200)
        self.assertLessEqual(thumb.height, 200)
