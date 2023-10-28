import django.db.models as dj_models
from django.shortcuts import HttpResponse, render  # noqa: F401
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers
from .models import Room
from .serializers import CreateRoomSerializer, RoomSerializer


class RoomView(generics.CreateAPIView):  # noqa: D101
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):  # noqa: D101
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()

            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return None

class RetailerViewSet(viewsets.ModelViewSet):
    """A view-set for retailers."""

    serializer_class = serializers.RetailerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> dj_models.QuerySet[models.Retailer]:
        """Get all retailers a user has access to."""
        user = self.request.user
        if not user.is_authenticated or not isinstance(user, models.User):
            return models.Retailer.objects.none()
        permission_group: models.FilePermissionGroup | None = user.permission_group
        if not permission_group:
            return models.Retailer.objects.none()
        if permission_group.retailers.filter(name="ALL").exists():
            return models.Retailer.objects.all()
        return permission_group.retailers.all()


class SupplierGroupViewSet(viewsets.ModelViewSet):
    """A view-set for supplier groups."""

    serializer_class = serializers.SupplierGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> dj_models.QuerySet[models.SupplierGroup]:
        """Get all files given a users retailer and supplier."""
        user = self.request.user
        if not user.is_authenticated or not isinstance(user, models.User):
            return models.SupplierGroup.objects.none()
        permission_group: models.FilePermissionGroup | None = user.permission_group
        if not permission_group:
            return models.SupplierGroup.objects.none()
        if permission_group.supplier_groups.filter(name="ALL").exists():
            return models.SupplierGroup.objects.all()
        return permission_group.supplier_groups.all()


class FileTypeViewSet(viewsets.ModelViewSet):
    """A view-set for supplier groups."""

    serializer_class = serializers.FileTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> dj_models.QuerySet[models.FileType]:
        """Get all files given a users retailer and supplier."""
        user = self.request.user
        if not user.is_authenticated or not isinstance(user, models.User):
            return models.FileType.objects.none()
        permission_group: models.FilePermissionGroup | None = user.permission_group
        if not permission_group:
            return models.FileType.objects.none()
        if permission_group.file_types.filter(name="ALL").exists():
            return models.FileType.objects.all()
        return permission_group.file_types.all()


class FileViewSet(viewsets.ModelViewSet):
    """A view-set for files. Takes into account user permissions."""

    serializer_class = serializers.FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> dj_models.QuerySet[models.File]:
        """Get all files given a users retailer and supplier."""
        user = self.request.user
        file_manager: dj_models.Manager[models.File] = models.File.objects
        if not user.is_authenticated or not isinstance(user, models.User):
            return file_manager.none()
        permission_group: models.FilePermissionGroup | None = user.permission_group
        if not permission_group:
            return file_manager.none()
        queryset = file_manager.all()
        if not permission_group.retailers.filter(name="ALL").exists():
            queryset = queryset.filter(retailer__in=permission_group.retailers.all())
        if not permission_group.supplier_groups.filter(name="ALL").exists():
            queryset = queryset.filter(supplier_group__in=permission_group.supplier_groups.all())
        if not permission_group.file_types.filter(name="ALL").exists():
            queryset = queryset.filter(file_type__in=permission_group.file_types.all())
        return queryset


class NotificationLogViewSet(viewsets.ModelViewSet):
    """A view-set for notification logs."""

    serializer_class = serializers.NotificationLogSerializer
    queryset = models.NotificationLog.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """A view-set for notification logs."""

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
