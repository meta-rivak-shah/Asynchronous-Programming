from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from datetime import datetime, date, timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
"""
"""


class EmailVerificationManager(BaseUserManager):
    def create_email_confirmation(self, user_id, invitation_token, expired_at, email):
        email_confirm = self.model(
            email=self.normalize_email( email ),
            user_id_id=user_id,
            email_token=invitation_token,
            expiration_at=expired_at
        )
        email_confirm.created_by_id = user_id
        email_confirm.save(using=self._db)
        return email_confirm

    def create_email_invitation_form(self, user_data):
        user_id = user_data.id
        expired_at = datetime.utcnow() + relativedelta(minute=15)
        email_confirm = self.create_email_confirmation(
            user_id,
            user_data.invitation_token,
            expired_at,
            user_data.email,
        )
        email_confirm.created_on = datetime.utcnow()
        email_confirm.save(using=self._db)
        return email_confirm
