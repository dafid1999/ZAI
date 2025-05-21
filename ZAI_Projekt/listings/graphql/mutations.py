import graphene
import graphql_jwt
from ..models import Listing, Category, Tag
from .types import ListingType, ProfileType

class CreateListing(graphene.Mutation):
    listing = graphene.Field(ListingType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        price = graphene.Float(required=True)
        category_name = graphene.String(required=True)
        tag_names = graphene.List(graphene.String)
        expires_at = graphene.DateTime()

    def mutate(self, info, title, description, price, category_name, tag_names=None, expires_at=None):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise Exception("Authentication required")
        cat, _ = Category.objects.get_or_create(name=category_name)
        listing = Listing(
            title=title,
            description=description,
            price=price,
            author=user,
            category=cat,
            expires_at=expires_at
        )
        listing.save()
        if tag_names:
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                listing.tags.add(tag)
        return CreateListing(listing=listing)

class UpdateListing(graphene.Mutation):
    listing = graphene.Field(ListingType)

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        price = graphene.Float()
        status = graphene.String()
        category_name = graphene.String()
        tag_names = graphene.List(graphene.String)
        expires_at = graphene.DateTime()

    def mutate(self, info, id, **kwargs):
        user = info.context.user
        listing = Listing.objects.get(pk=id)
        if listing.author != user and not user.is_staff and not user.groups.filter(name='moderators').exists():
            raise Exception("Not permitted to update this listing")
        for field, value in kwargs.items():
            if field == 'category_name':
                cat, _ = Category.objects.get_or_create(name=value)
                listing.category = cat
            elif field == 'tag_names':
                listing.tags.clear()
                for name in value:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    listing.tags.add(tag)
            else:
                setattr(listing, field, value)
        listing.save()
        return UpdateListing(listing=listing)

class DeleteListing(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        user = info.context.user
        listing = Listing.objects.get(pk=id)
        if listing.author != user and not user.is_staff and not user.groups.filter(name='moderators').exists():
            raise Exception("Not permitted to delete this listing")
        listing.delete()
        return DeleteListing(ok=True)

class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(ProfileType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)