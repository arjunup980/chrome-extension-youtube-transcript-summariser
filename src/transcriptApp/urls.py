from django.urls import path
from .views import TranscriptView

urlpatterns = [
    path('', TranscriptView.as_view(), name='transcript'),
]
