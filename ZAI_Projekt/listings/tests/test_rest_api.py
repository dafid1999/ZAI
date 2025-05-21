from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from rest_framework import status
from listings.models import Category, Tag, Listing, Profile

class ListingAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        self.other_user = User.objects.create_user(username='user2', password='pass')
        self.mod = User.objects.create_user(username='mod', password='pass')
        moderators_group = Group.objects.create(name='moderators')
        self.mod.groups.add(moderators_group)
        self.admin = User.objects.create_superuser(username='admin', password='pass')

        self.cat = Category.objects.create(name='Electronics')
        self.tag = Tag.objects.create(name='Sale')

        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'username':'user1','password':'pass'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")

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

    def test_owner_can_update(self):
        listing = Listing.objects.create(
            title='Old', description='Desc', price=5.0,
            author=self.user, category=self.cat, status='PENDING'
        )
        url = reverse('listing-detail', args=[listing.pk])
        data = {'title':'New' }
        resp = self.client.patch(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        listing.refresh_from_db()
        self.assertEqual(listing.title, 'New')

    def test_non_owner_cannot_update(self):
        url_token = reverse('token_obtain_pair')
        resp = self.client.post(url_token, {'username':'user2','password':'pass'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")
        listing = Listing.objects.create(
            title='Old', description='Desc', price=5.0,
            author=self.user, category=self.cat, status='PENDING'
        )
        url = reverse('listing-detail', args=[listing.pk])
        resp = self.client.patch(url, {'title':'Hack'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_update(self):
        url_token = reverse('token_obtain_pair')
        resp = self.client.post(url_token, {'username':'mod','password':'pass'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")
        listing = Listing.objects.create(
            title='Old', description='Desc', price=5.0,
            author=self.user, category=self.cat, status='PENDING'
        )
        url = reverse('listing-detail', args=[listing.pk])
        resp = self.client.patch(url, {'status':'APPROVED'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        listing.refresh_from_db()
        self.assertEqual(listing.status, 'APPROVED')

    def test_owner_can_delete(self):
        listing = Listing.objects.create(
            title='ToDelete', description='Desc', price=5.0,
            author=self.user, category=self.cat, status='PENDING'
        )
        url = reverse('listing-detail', args=[listing.pk])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Listing.objects.filter(pk=listing.pk).exists())

    def test_non_owner_cannot_delete(self):
        url_token = reverse('token_obtain_pair')
        resp = self.client.post(url_token, {'username':'user2','password':'pass'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")
        listing = Listing.objects.create(
            title='ToDelete', description='Desc', price=5.0,
            author=self.user, category=self.cat, status='PENDING'
        )
        url = reverse('listing-detail', args=[listing.pk])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_delete(self):
        url_token = reverse('token_obtain_pair')
        resp = self.client.post(url_token, {'username':'mod','password':'pass'}, format='json')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")
        listing = Listing.objects.create(
            title='ToDelete', description='Desc', price=5.0,
            author=self.user, category=self.cat, status='PENDING'
        )
        url = reverse('listing-detail', args=[listing.pk])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)


class ListingFilterTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass')
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'username': 'user1', 'password': 'pass'}, format='json')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        self.cat = Category.objects.create(name='Electronics')
        self.tag = Tag.objects.create(name='Sale')

        Listing.objects.create(
            title='Pending Ad', description='P', price=1.0,
            author=self.user, category=self.cat, status='PENDING'
        )
        approved = Listing.objects.create(
            title='Approved Ad', description='A', price=2.0,
            author=self.user, category=self.cat, status='APPROVED'
        )
        approved.tags.add(self.tag)

    def test_filter_by_status(self):
        url = reverse('listing-list') + '?status=APPROVED'
        resp = self.client.get(url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        data = resp.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'APPROVED')
        self.assertEqual(data[0]['title'], 'Approved Ad')

