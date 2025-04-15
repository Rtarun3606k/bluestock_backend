from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, IPO, UserProfile
from .serializers import CompanySerializer, IPOSerializer, UserProfileSerializer
from django.utils import timezone

# Create your views here.

class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for companies
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class IPOViewSet(viewsets.ModelViewSet):
    """
    API endpoint for IPOs
    """
    queryset = IPO.objects.all()
    serializer_class = IPOSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'company']
    search_fields = ['company__name', 'issue_type']
    ordering_fields = ['open_date', 'close_date', 'listing_date', 'issue_size']

    def get_queryset(self):
        """
        Optionally filter IPOs by status
        """
        queryset = IPO.objects.all()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter for upcoming IPOs
        upcoming = self.request.query_params.get('upcoming')
        if upcoming:
            today = timezone.now().date()
            queryset = queryset.filter(open_date__gte=today)
        
        # Filter for currently open IPOs
        open_now = self.request.query_params.get('open_now')
        if open_now:
            today = timezone.now().date()
            queryset = queryset.filter(open_date__lte=today, close_date__gte=today)
            
        return queryset

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for user profiles (read-only)
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Users can only view their own profile unless they're staff/admin
        """
        user = self.request.user
        if user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=user)
