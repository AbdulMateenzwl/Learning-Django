from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from . import api_views

urlpatterns = [
    # JWT Token endpoints
    path('api/token/', api_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User management endpoints
    path('api/register/', api_views.register_user, name='api_register'),
    path('api/logout/', api_views.logout_user, name='api_logout'),
    path('api/profile/', api_views.user_profile, name='api_profile'),
    path('api/profile/update/', api_views.update_profile, name='api_update_profile'),
]
