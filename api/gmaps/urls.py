from django.urls import path
from .views import HealthCheckView

urlpatterns = [
    path('health_check/', HealthCheckView.as_view(), name='health_check'),
]
