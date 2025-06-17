from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import RegisterView, MyTokenObtainPairView, UpdateProfileImageView, UserDetailView, ChangePasswordView

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/",TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("user/image/", UpdateProfileImageView.as_view(), name="update-profile-image"),
    path('user/me/', UserDetailView.as_view(), name='user-detail'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
