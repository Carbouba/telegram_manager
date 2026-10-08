from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import DialogViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'dialogs', DialogViewSet)
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = [path('', include(router.urls))]