from django.db.models import Avg, Count
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ListingSerializer, CategorySerializer, TagSerializer, ProfileSerializer
from ..models import Listing, Category, Tag, Profile
from ..permissions import IsOwnerOrAdminOrModerator


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrModerator]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'tags', 'author']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    @action(detail=False, methods=["get"], url_path="statistics", permission_classes=[permissions.IsAuthenticated])
    def statistics(self, request):
        total = Listing.objects.count()
        avg_price = Listing.objects.aggregate(avg=Avg("price"))["avg"]

        by_category = (
            Category.objects.annotate(count=Count("listings"))
            .values("name", "count")
        )

        by_status = (
            Listing.objects.values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        )

        return Response({
            "total_listings": total,
            "average_price": avg_price,
            "listings_by_category": list(by_category),
            "listings_by_status": list(by_status),
        })


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAdminUser]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]