from uuid import uuid4
from django.db import models
from django.utils import timezone


class IdWrapper(models.Model):
    """
    Abstract Model providing id encapsulating all models
    """
    id = models.UUIDField(primary_key=True, default=uuid4, unique=True)

    class Meta:
        abstract = True


class DeletableWrapper(models.Model):
    """
    Model for managing delete events
    """
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey('CustomUser.CustomUserModel', related_name='%(class)s_deleted_by', blank=True,
                                   null=True, on_delete=models.CASCADE)

    def delete(self, user=None):
        if self.is_deleted:
            return None
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save()

    class Meta:
        abstract = True


class CustomModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('CustomUser.CustomUserModel', related_name='%(class)s_created_by',
                                   on_delete=models.CASCADE)

    class Meta:
        abstract = True


# class UpdatedWrapper(models.Model):
#     updated_at = models.DateTimeField(auto_now=True)
#     updated_by = models.ForeignKey('CustomUser.CustomUserModel', related_name='%(class)s_updated_by',
#                                    on_delete=models.CASCADE, null=True, blank=True)
#
#     class Meta:
#         abstract: True
