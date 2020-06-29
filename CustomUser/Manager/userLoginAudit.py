from django.contrib.auth.models import BaseUserManager


class LoginAuditLogManager(BaseUserManager):
    def create_audit_log(self, user=None, email=None, ip=None, HTTP_ORIGIN=None, status=None):
        audit_obj = self.create(
            ip=ip,
            HTTP_ORIGIN=HTTP_ORIGIN
        )
        return audit_obj
