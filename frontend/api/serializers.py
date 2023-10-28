from rest_framework import serializers

from . import models
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for the Room model."""

    class Meta:
        """Serializer metadata."""

        model = Room
        fields = ("id", "code", "host", "guest_can_pause",
                  "votes_to_skip", "created_at")

class CreateRoomSerializer(serializers.ModelSerializer):
    """Serialiser for CreateRoom model."""

    class Meta:
        """Serializer metadata."""

        model = Room
        fields = ("guest_can_pause", "votes_to_skip")


class SupplierGroupSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the SupplierGroup model."""

    class Meta:
        """Serializer metadata."""

        model = models.SupplierGroup
        exclude: list[str] = []


class RetailerSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the Retailer model."""

    class Meta:
        """Serializer metadata."""

        model = models.Retailer
        exclude: list[str] = []


class FileSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the File model."""

    class Meta:
        """Serializer metadata."""

        model = models.File
        exclude: list[str] = []


class NotificationLogSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the NotificationLog model."""

    class Meta:
        """Serializer metadata."""

        model = models.NotificationLog
        exclude: list[str] = []


class FileTypeSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the FileType model."""

    class Meta:
        """Serializer metadata."""

        model = models.FileType
        exclude: list[str] = []


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the User model."""

    class Meta:
        """Serializer metadata."""

        model = models.User
        exclude: list[str] = []
