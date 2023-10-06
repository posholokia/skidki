from django.urls import path, include, re_path
from rest_framework import routers
from .views import UserEmailChange

router = routers.DefaultRouter()
router.register(r"auth/users/me", UserEmailChange)


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
]
urlpatterns += router.urls