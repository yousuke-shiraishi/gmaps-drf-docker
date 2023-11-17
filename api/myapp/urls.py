from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from gmaps.views import UserViewSet, GmapViewSet, HealthCheckView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'gmaps', GmapViewSet, basename='gmaps')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('health_check/', HealthCheckView.as_view(), name='health_check'),
    path('gmaps/public_search/', GmapViewSet.as_view({'get': 'public_search'}), name='public_search'),
    path('gmaps/private_search/', GmapViewSet.as_view({'get': 'private_search'}), name='private_search'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/', include('djoser.urls.authtoken')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


