from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, IPOViewSet, UserProfileViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'ipos', IPOViewSet)
router.register(r'profiles', UserProfileViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]