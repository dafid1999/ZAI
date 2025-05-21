import graphene
from listings.graphql.queries import Query as ListingsQuery
from listings.graphql.mutations import (
    CreateListing, UpdateListing, DeleteListing, ObtainJSONWebToken
)
import graphql_jwt

class Mutation(ListingsQuery, graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()
    create_listing = CreateListing.Field()
    update_listing = UpdateListing.Field()
    delete_listing = DeleteListing.Field()

schema = graphene.Schema(
    query=ListingsQuery,
    mutation=Mutation
)