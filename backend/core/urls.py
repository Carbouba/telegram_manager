from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import DialogViewSet

router = DefaultRouter()
router.register(r'dialogs', DialogViewSet)

urlpatterns = [path('', include(router.urls))]