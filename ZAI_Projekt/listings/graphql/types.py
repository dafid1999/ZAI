import graphene
from graphene_django.types import DjangoObjectType
from ..models import Listing, Category, Tag, Profile

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ('id', 'name')

class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ('id', 'name')

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ('user', 'phone_number')

class ListingType(DjangoObjectType):
    class Meta:
        model = Listing
        fields = (
            'id', 'title', 'description', 'price', 'status',
            'created_at', 'updated_at', 'expires_at',
            'author', 'category', 'tags', 'image', 'favorited_by'
        )