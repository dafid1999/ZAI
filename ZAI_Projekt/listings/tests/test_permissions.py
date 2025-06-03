from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from listings.models import Listing, Category
from rest_framework import status


class ListingPermissionTestCase(APITestCase):
    def setUp(self):
        # Grupa moderatorów
        self.moderators = Group.objects.create(name='moderators')

        # Użytkownicy
        self.author = User.objects.create_user(username='author', password='pass')
        self.other_user = User.objects.create_user(username='other', password='pass')
        self.staff = User.objects.create_user(username='staff', password='pass', is_staff=True)
        self.moderator = User.objects.create_user(username='mod', password='pass')
        self.moderator.groups.add(self.moderators)

        # Kategorie
        self.cat = Category.objects.create(name='Electronics')

        # Ogłoszenie
        self.listing = Listing.objects.create(
            title='Test Ad',
            description='Some description',
            price=10.00,
            category=self.cat,
            author=self.author,
            status='PENDING'
        )

        self.url = reverse('listing-detail', args=[self.listing.id])

    def authenticate(self, user):
        resp = self.client.post(reverse('token_obtain_pair'), {'username': user.username, 'password': 'pass'}, format='json')
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_owner_can_update(self):
        self.authenticate(self.author)
        resp = self.client.patch(self.url, {'title': 'Updated Title'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_staff_can_update(self):
        self.authenticate(self.staff)
        resp = self.client.patch(self.url, {'title': 'Updated by staff'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_moderator_can_update(self):
        self.authenticate(self.moderator)
        resp = self.client.patch(self.url, {'title': 'Updated by mod'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_update(self):
        self.authenticate(self.other_user)
        resp = self.client.patch(self.url, {'title': 'Hacked'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_update(self):
        self.client.credentials()
        resp = self.client.patch(self.url, {'title': 'Anon update'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_can_delete(self):
        self.authenticate(self.author)
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_staff_can_delete(self):
        self.authenticate(self.staff)
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_moderator_can_delete(self):
        self.authenticate(self.moderator)
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_other_user_cannot_delete(self):
        self.authenticate(self.other_user)
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_delete(self):
        self.client.credentials()
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

