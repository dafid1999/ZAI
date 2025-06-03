from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from listings.models import Category, Tag, Listing, Profile

class ListingAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        self.mod = User.objects.create_user(username='mod', password='pass', is_staff=True)
        self.cat = Category.objects.create(name='Electronics')
        self.tag = Tag.objects.create(name='Sale')
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'username':'user1','password':'pass'}, format='json')
        self.token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_listing(self):
        url = reverse('listing-list')
        data = {
            'title':'Test', 'description':'Desc', 'price':'10.00',
            'category':'Electronics', 'tags':['Sale'], 'expires_at':'2025-06-01T00:00:00Z'
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Listing.objects.count(), 1)

    def test_unauthenticated_cannot_create(self):
        self.client.force_authenticate(user=None)
        url = reverse('listing-list')
        resp = self.client.post(url, {}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)