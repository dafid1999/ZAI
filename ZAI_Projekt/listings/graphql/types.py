import graphene
from graphene_django import DjangoObjectType
from listings.models import Listing, Category, Tag, Profile

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "listings")

class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ("id", "name", "listings")

class ListingType(DjangoObjectType):
    class Meta:
        model = Listing
        fields = (
            "id", "title", "description", "price", "status", 
            "created_at", "updated_at", "expires_at", 
            "author", "category", "tags", "image", "thumbnail"
        )

class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ("user", "phone_number")
