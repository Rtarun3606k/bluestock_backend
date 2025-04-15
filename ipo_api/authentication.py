from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import UserProfile


class ApiKeyAuthentication(BaseAuthentication):
    """
    Custom authentication class for API key authentication
    """

    def authenticate(self, request):
        # Get the API key from the request headers
        api_key = request.META.get('HTTP_X_API_KEY')
        if not api_key:
            return None  # No API key provided, let other authentication methods handle it
            
        # Find the user profile with the given API key
        try:
            user_profile = UserProfile.objects.get(api_key=api_key)
            if not user_profile.is_client:
                raise AuthenticationFailed('API key is not associated with a client account')
            
            return (user_profile.user, None)  # Authentication successful
        except UserProfile.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')