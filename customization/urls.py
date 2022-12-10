from django.urls import path
from .views import CustomRendererAPIView

urlpatterns = [
    path('renderers/', CustomRendererAPIView.as_view())
]
