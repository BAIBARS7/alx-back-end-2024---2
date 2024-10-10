from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

# Create a router and register the ReviewViewSet with it
router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Include all routes from the router under 'api/'
]
