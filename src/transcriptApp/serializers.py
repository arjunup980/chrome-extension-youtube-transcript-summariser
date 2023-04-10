from rest_framework import serializers

class TranscriptSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=200)
