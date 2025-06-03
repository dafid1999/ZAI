import graphene
import graphql_jwt
from listings.graphql.queries import Query as ListingsQuery
from listings.graphql.mutations import (
    CreateListing,
    UpdateListing,
    DeleteListing,
    CreateCategory,
    UpdateCategory,
    DeleteCategory,
    CreateTag,
    UpdateTag,
    DeleteTag,
    UpdateProfile
)
from users.graphql.mutations import RegisterUser


class Mutation(
    ListingsQuery,
    graphene.ObjectType
):
    # JWT
    tokenAuth = graphql_jwt.ObtainJSONWebToken.Field()
    refreshToken = graphql_jwt.Refresh.Field()
    verifyToken = graphql_jwt.Verify.Field()

    # Listings
    createListing = CreateListing.Field()
    updateListing = UpdateListing.Field()
    deleteListing = DeleteListing.Field()

    # Category
    createCategory = CreateCategory.Field()
    updateCategory = UpdateCategory.Field()
    deleteCategory = DeleteCategory.Field()

    # Tag
    createTag = CreateTag.Field()
    updateTag = UpdateTag.Field()
    deleteTag = DeleteTag.Field()

    # Profile
    updateProfile = UpdateProfile.Field()

    # User Registration
    registerUser = RegisterUser.Field()

schema = graphene.Schema(query=ListingsQuery, mutation=Mutation)
