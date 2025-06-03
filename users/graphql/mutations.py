import graphene
from django.contrib.auth.models import User, Group
from graphql import GraphQLError
from graphene_django.types import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class RegisterUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    user = graphene.Field(UserType)

    def mutate(self, info, username, email, password):
        errors = []
        if User.objects.filter(username=username).exists():
            errors.append("Username already taken.")
        if User.objects.filter(email=email).exists():
            errors.append("Email already in use.")
        if errors:
            return RegisterUser(success=False, errors=errors, user=None)

        user = User(username=username, email=email)
        user.set_password(password)
        user.full_clean()
        user.save()

        default_group, _ = Group.objects.get_or_create(name="user")
        user.groups.add(default_group)

        return RegisterUser(success=True, errors=None, user=user)
