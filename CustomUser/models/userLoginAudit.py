from datetime import datetime
from django.utils import timezone
from django.db import models
from CommonApp import constants
from CustomUser.Manager.userLoginAudit import LoginAuditLogManager


class LoginAuditLogModel(models.Model):
    user = models.ForeignKey('CustomUser.CustomUserModel', related_name='%(class)s_user_id', null=True, blank=True,
                             on_delete=models.CASCADE)
    email = models.CharField(max_length=128, null=True, blank=True)
    ip = models.CharField(max_length=128, null=True, blank=True)
    HTTP_ORIGIN = models.CharField(max_length=256, null=True, blank=True)
    status = models.CharField( max_length=128, choices=constants.LOGIN_STATUS)
    timestamp = models.DateTimeField( null=True, blank=True )
    exception = models.CharField(max_length=50, blank=True)

    objects = LoginAuditLogManager()

    def update_log(self, status=None, user=None, email=None, exception=None):
        self.user = user
        self.email = email
        self.status = status
        self.timestamp = timezone.now()
        self.exception = exception
        self.save()
