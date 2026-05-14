from rest_framework import serializers
from .models import Notification
# Serializer for converting Notification model instances into JSON-friendly data
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        # The model this serializer is based on
        model = Notification
        # Fields that will be included in the API response
        fields = [
            'id',         # Unique identifier for the notification
            'message',    # Text content of the notification
            'is_read',    # Whether the user has opened/read it
            'created_at', # Timestamp when the notification was created
        ]
