import graphene
from ..models import Listing, Category, Tag, Profile
from .types import ListingType, CategoryType, TagType, ProfileType

class Query(graphene.ObjectType):
    all_listings = graphene.List(ListingType, status=graphene.String())
    listing = graphene.Field(ListingType, id=graphene.Int(required=True))
    all_categories = graphene.List(CategoryType)
    all_tags = graphene.List(TagType)
    me = graphene.Field(ProfileType)

    def resolve_all_listings(root, info, status=None):
        qs = Listing.objects.all()
        if status:
            qs = qs.filter(status=status)
        return qs

    def resolve_listing(root, info, id):
        return Listing.objects.get(pk=id)

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_all_tags(root, info):
        return Tag.objects.all()

    def resolve_me(root, info):
        user = info.context.user
        return Profile.objects.get(user=user)