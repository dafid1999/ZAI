from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, CategoryViewSet, TagViewSet, ProfileViewSet

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = router.urls