from django.urls import path
from . import views

urlpatterns = [
    path('reviews/', views.ReviewAPIView.as_view(), name='api-reviews'),
]