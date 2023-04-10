from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from transcript.decorators import log_time
from .serializers import TranscriptSerializer
from .service import TranscriptService

class TranscriptView(APIView):
    service = TranscriptService()
    serializer = TranscriptSerializer

    @log_time
    @method_decorator(cache_page(86400))
    def get(self, request: Request):
        serializer = self.serializer(data=request.GET)

        if serializer.is_valid():
            response = self.service.get_summary(youtube_url=serializer.validated_data.get('url'))
            return Response(response)
        else:
            return Response(serializer.errors, status=400)
