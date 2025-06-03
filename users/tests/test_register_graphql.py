import json
from django.test import TestCase, Client
from django.contrib.auth.models import Group, User

class RegisterGraphQLTest(TestCase):
    GRAPHQL_URL = "/graphql/"

    def setUp(self):
        Group.objects.get_or_create(name="user")
        self.client = Client()

    def test_register_user_success(self):
        mutation = """
        mutation {
          registerUser(
            username: "graphqluser",
            email: "graphql@example.com",
            password: "securepass"
          ) {
            success
            errors
            user {
              id
              username
              email
            }
          }
        }
        """
        resp = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({"query": mutation}),
            content_type="application/json"
        )
        content = json.loads(resp.content)
        data = content["data"]["registerUser"]
        self.assertTrue(data["success"])
        self.assertIsNone(data["errors"])
        self.assertEqual(data["user"]["username"], "graphqluser")
        self.assertTrue(User.objects.filter(username="graphqluser").exists())
        # Sprawdź, że nowy użytkownik ma przypisaną grupę 'user'
        user = User.objects.get(username="graphqluser")
        self.assertTrue(user.groups.filter(name="user").exists())

    def test_register_user_duplicate_username(self):
        # Stwórz istniejącego użytkownika
        User.objects.create_user(username="exists", email="x@x.com", password="pass")
        Group.objects.get_or_create(name="user")

        mutation = """
        mutation {
          registerUser(
            username: "exists",
            email: "newemail@example.com",
            password: "securepass"
          ) {
            success
            errors
            user {
              id
              username
              email
            }
          }
        }
        """
        resp = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({"query": mutation}),
            content_type="application/json"
        )
        content = json.loads(resp.content)
        data = content["data"]["registerUser"]
        self.assertFalse(data["success"])
        self.assertIn("Username already taken.", data["errors"])
        self.assertIsNone(data["user"])
