import random
import string
from pathlib import Path
from typing import Any

from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager, PermissionsMixin  # noqa: F401
from django.db import models
from django.utils import timezone


def generate_unique_code() -> int:
    """Return an int with a randomly generated code."""
    length = 6

    while True:
        code = "".join(random.choices(string.ascii_uppercase, k=length))  # noqa: S311
        if Room.objects.filter(code=code).count() == 0:
            break

    return code


# Create your models here.
class Room(models.Model):  # noqa: DJ008, D101
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)




#The below classes are for Portal
class SupplierGroup(models.Model):
    """Group of Suppliers. Can encompass multiple SupplierIDs."""

    name = models.CharField(max_length=255)
    extended_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return string representation to be used by django admin."""
        return f"{self.name}"


class Retailer(models.Model):
    """Retailer. A Retailer of 'All' allows for all retailers. Will generally only be given to superusers."""

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return string representation to be used by django admin."""
        return f"{self.name}"


class UserManager(BaseUserManager):
    """Custom manager for Users to ensure they have a specified email address."""

    def _create_user(
        self,
        email: str,
        password: str,
        *,
        is_staff: bool,
        is_superuser: bool,
        **extra_fields: dict[str, Any],
    ) -> "User":
        if not email:
            msg = "Users must have an email address"
            raise ValueError(msg)
        now = timezone.now()
        email = self.normalize_email(email)
        user: "User" = self.model(  # type: ignore[assignment]
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            created_at=now,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields: dict[str, Any]) -> "User":
        """Create a non staff non superuser user."""
        return self._create_user(email, password, is_staff=False, is_superuser=False, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: dict[str, Any]) -> "User":
        """Create a superuser."""
        user = self._create_user(email, password, is_staff=True, is_superuser=True, **extra_fields)
        user.save(using=self._db)
        return user


class FileType(models.Model):
    """Type of file."""

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return string representation to be used by django admin."""
        return f"{self.name}"


class FilePermissionGroup(models.Model):
    """Collection of references to different categories of files a user has access to.

    The list of files they have access to is based on an intersection of all the filters.
    """

    name = models.CharField(max_length=254, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    supplier_groups = models.ManyToManyField(SupplierGroup, related_name="file_permission_groups")
    retailers = models.ManyToManyField(Retailer, related_name="file_permission_groups")
    file_types = models.ManyToManyField(FileType, related_name="file_permission_groups")

    def __str__(self) -> str:
        """Return string representation to be used by django admin."""
        return f"{self.name}"


class User(models.Model):  # noqa: DJ008
#class User(AbstractBaseUser, PermissionsMixin): #, guardian.mixins.GuardianUserMixin):
    """User override."""

    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    permission_group = models.ForeignKey(FilePermissionGroup, on_delete=models.SET_NULL, null=True)
    email_notifications = models.BooleanField(default=True)
    account_manager = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, related_name="managed_users")

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self: "User") -> str:
        """Get absolute url of a user."""
        return f"/users/{self.pk}/"


class TagCategory(models.Model):
    """categories file tags sit under."""

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    parent_category = models.ForeignKey(
        "TagCategory",
        on_delete=models.CASCADE,
        related_name="child_categories",
        null=True,
    )

    def __str__(self) -> str:
        """Return string representation to be used by django admin."""
        return f"{self.name}"


class Tag(models.Model):
    """categorisation tag for a file."""

    code = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(TagCategory, on_delete=models.CASCADE)
    parent_tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="child_tags", null=True)

    def __str__(self) -> str:
        """Return string representation to be used by django admin."""
        if len(self.code) > 0:
            return f"{self.description} - ({self.code})"
        return f"{self.description}"


class File(models.Model):
    """Portal File."""

    file_path = models.FilePathField(path="/home/portal_files")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    report_data_date = models.DateField()
    file_creation_datetime = models.DateTimeField(default=timezone.now)
    supplier_group = models.ForeignKey(SupplierGroup, on_delete=models.CASCADE)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    file_type = models.ForeignKey(FileType, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, related_name="files")

    def __str__(self) -> str:
        """Return string representation to be used by django admin."""
        return f"{Path(self.file_path).name}"


class NotificationLog(models.Model):
    """Log of notification send out."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_data_date = models.DateField()
    send_time = models.DateTimeField(auto_now_add=True)
    delivery_response_time = models.DateTimeField(null=True)
    delivery_response_event_type = models.CharField(max_length=255)
    delivery_response_bounce_type = models.CharField(max_length=255)
    delivery_response_bounce_sub_type = models.CharField(max_length=255)

    def __str__(self) -> str:
        """Return string representation to be used by django admin."""
        return f"{self.user}-{self.report_data_date}"
