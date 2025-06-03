import graphene
import graphql_jwt
from decimal import Decimal
from listings.models import Listing, Category, Tag, Profile
from .types import ListingType, CategoryType, TagType, ProfileType

class CreateListing(graphene.Mutation):
    listing = graphene.Field(ListingType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        price = graphene.Float(required=True)
        category_name = graphene.String(required=True)
        tag_names = graphene.List(graphene.String)
        expires_at = graphene.DateTime()
        image = graphene.String()

    def mutate(self, info, title, description, price, category_name, tag_names=None, expires_at=None, image=None):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise Exception("Authentication required")

        cat, _ = Category.objects.get_or_create(name=category_name)
        listing = Listing(
            title=title,
            description=description,
            price=Decimal(str(price)),
            author=user,
            category=cat,
            expires_at=expires_at
        )
        if image:
            listing.image = image
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
        image = graphene.String()

    def mutate(self, info, id, **kwargs):
        user = info.context.user
        try:
            listing = Listing.objects.get(pk=id)
        except Listing.DoesNotExist:
            raise Exception("Listing not found")
        if listing.author != user and not user.is_staff and not user.groups.filter(name="moderators").exists():
            raise Exception("Not permitted to update this listing")

        if "title" in kwargs and kwargs["title"] is not None:
            listing.title = kwargs["title"]
        if "description" in kwargs and kwargs["description"] is not None:
            listing.description = kwargs["description"]
        if "price" in kwargs and kwargs["price"] is not None:
            listing.price = Decimal(str(kwargs["price"]))
        if "status" in kwargs and kwargs["status"] is not None:
            listing.status = kwargs["status"]
        if "expires_at" in kwargs and kwargs["expires_at"] is not None:
            listing.expires_at = kwargs["expires_at"]
        if "image" in kwargs and kwargs["image"] is not None:
            listing.image = kwargs["image"]
        if "category_name" in kwargs and kwargs["category_name"] is not None:
            cat, _ = Category.objects.get_or_create(name=kwargs["category_name"])
            listing.category = cat
        if "tag_names" in kwargs and kwargs["tag_names"] is not None:
            listing.tags.clear()
            for name in kwargs["tag_names"]:
                tag, _ = Tag.objects.get_or_create(name=name)
                listing.tags.add(tag)

        listing.save()
        return UpdateListing(listing=listing)

class DeleteListing(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        user = info.context.user
        try:
            listing = Listing.objects.get(pk=id)
        except Listing.DoesNotExist:
            raise Exception("Listing not found")
        if listing.author != user and not user.is_staff and not user.groups.filter(name="moderators").exists():
            raise Exception("Not permitted to delete this listing")
        listing.delete()
        return DeleteListing(ok=True)

# -----------------------------
# CRUD Category
# -----------------------------

class CreateCategory(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        user = info.context.user
        if not user or not user.is_authenticated or not user.is_staff:
            raise Exception("Admin privileges required")
        cat, created = Category.objects.get_or_create(name=name)
        if not created:
            raise Exception("Category with this name already exists")
        return CreateCategory(category=cat)

class UpdateCategory(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    def mutate(self, info, id, name):
        user = info.context.user
        if not user or not user.is_authenticated or not user.is_staff:
            raise Exception("Admin privileges required")
        try:
            cat = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            raise Exception("Category not found")
        if Category.objects.filter(name=name).exclude(pk=id).exists():
            raise Exception("Category with this new name already exists")
        cat.name = name
        cat.save()
        return UpdateCategory(category=cat)

class DeleteCategory(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        user = info.context.user
        if not user or not user.is_authenticated or not user.is_staff:
            raise Exception("Admin privileges required")
        try:
            cat = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            raise Exception("Category not found")
        cat.delete()
        return DeleteCategory(ok=True)

# -----------------------------
# CRUD Tag
# -----------------------------

class CreateTag(graphene.Mutation):
    tag = graphene.Field(TagType)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        user = info.context.user
        if not user or not user.is_authenticated or not user.is_staff:
            raise Exception("Admin privileges required")
        tag, created = Tag.objects.get_or_create(name=name)
        if not created:
            raise Exception("Tag with this name already exists")
        return CreateTag(tag=tag)

class UpdateTag(graphene.Mutation):
    tag = graphene.Field(TagType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    def mutate(self, info, id, name):
        user = info.context.user
        if not user or not user.is_authenticated or not user.is_staff:
            raise Exception("Admin privileges required")
        try:
            tag = Tag.objects.get(pk=id)
        except Tag.DoesNotExist:
            raise Exception("Tag not found")
        if Tag.objects.filter(name=name).exclude(pk=id).exists():
            raise Exception("Tag with this new name already exists")
        tag.name = name
        tag.save()
        return UpdateTag(tag=tag)

class DeleteTag(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        user = info.context.user
        if not user or not user.is_authenticated or not user.is_staff:
            raise Exception("Admin privileges required")
        try:
            tag = Tag.objects.get(pk=id)
        except Tag.DoesNotExist:
            raise Exception("Tag not found")
        tag.delete()
        return DeleteTag(ok=True)

# -----------------------------
# Update Profile
# -----------------------------

class UpdateProfile(graphene.Mutation):
    profile = graphene.Field(ProfileType)

    class Arguments:
        phone_number = graphene.String(required=True)

    def mutate(self, info, phone_number):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise Exception("Authentication required")
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise Exception("Profile not found")
        profile.phone_number = phone_number
        profile.save()
        return UpdateProfile(profile=profile)
