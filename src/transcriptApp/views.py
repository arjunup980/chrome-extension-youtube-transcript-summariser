from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from transcript.decorators import log_time
from .serializers import TranscriptSerializer
from .service import TranscriptService

class TranscriptView(APIView):
    service = TranscriptService()
    serializer = TranscriptSerializer

    @log_time
    def get(self, request: Request):
        serializer = self.serializer(data=request.GET)

        if serializer.is_valid():
            url = serializer.validated_data.get('url')
            refresh = serializer.validated_data.get('refresh')
            response = self.service.get_summary(youtube_url=url, refresh=refresh)
            return Response(response)
        else:
            return Response(serializer.errors, status=400)
