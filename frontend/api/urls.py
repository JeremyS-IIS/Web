from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"retailers", views.RetailerViewSet, basename="retailer")
router.register(r"supplier_groups", views.SupplierGroupViewSet, basename="suppliergroup")
router.register(r"files", views.FileViewSet, basename="file")
router.register(r"notification_logs", views.NotificationLogViewSet)
router.register(r"file_types", views.FileTypeViewSet, basename="file_type")
router.register(r"users", views.UserViewSet)

urlpatterns = [
    path("room", views.RoomView.as_view()),
    path("create-room", views.CreateRoomView.as_view()),
    path("portal", include(router.urls)),
]
