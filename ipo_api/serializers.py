from rest_framework import serializers
from .models import Company, IPO, UserProfile
from django.contrib.auth.models import User

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'logo', 'created_at']

class IPOSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source='company.name')
    company_logo = serializers.ImageField(source='company.logo', read_only=True)
    price_band = serializers.ReadOnlyField()
    listing_gain = serializers.ReadOnlyField()
    current_return = serializers.ReadOnlyField()
    
    class Meta:
        model = IPO
        fields = [
            'id', 'company', 'company_name', 'company_logo', 'price_band',
            'price_band_min', 'price_band_max', 'open_date', 'close_date',
            'issue_size', 'issue_type', 'listing_date', 'status',
            'ipo_price', 'listing_price', 'listing_gain',
            'current_market_price', 'current_return',
            'rhp_document', 'drhp_document', 'created_at'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone', 'is_client', 'api_key']
        read_only_fields = ['id', 'api_key']