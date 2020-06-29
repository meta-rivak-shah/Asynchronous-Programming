from django.db import models
from CommonApp.base import CustomModel
from CustomUser.Manager import EmailVerificationManager
from uuid import uuid4
from IntegrationsApp import send_email


class EmailConfirmationModel(CustomModel):
    user_id = models.ForeignKey( 'CustomUser.CustomUserModel', related_name='%(class)s_user_id',
                                 on_delete=models.CASCADE )
    email = models.EmailField()
    email_token = models.UUIDField()
    expiration_at = models.DateTimeField()
    is_expired = models.BooleanField( default=False )
    is_complete = models.BooleanField( default=False )
    updated_at = models.DateTimeField( auto_now=True )
    updated_by = models.ForeignKey( 'CustomUser.CustomUserModel', related_name='%(class)s_updated_by',
                                    on_delete=models.CASCADE, null=True, blank=True )
    objects = EmailVerificationManager()

    def __str__(self):
        return f"{self.email} - {self.email_token}"

    def send_email(self, email_type, email_receiver):
        if not self.email_token:
            access_token = uuid4()
            self.email_token = access_token
            self.save()

        keys = {
            'accountActivation': {
                'template': 'accountactivation.html',
                'subject': 'ACCOUNT ACTIVATION',
                'url': "http://127.0.0.1:8000/user/account_activation"
            }
        }.get( email_type, None )
        if keys is None:
            return False
        subject = keys.get( 'subject' )
        url = keys.get( 'url' ) + '?access_token={}&email={}'.format( self.email_token, self.email )
        template = keys.get( 'template' )

        context = {
            'email_receiver': email_receiver,
            'url': url,
            'name': self.user_id.get_full_name()
        }
        email = [email_receiver]
        status = send_email(
            RECIPIENT=email,
            SUBJECT=subject,
            TEMPLATEPATH=template,
            CONTEXT=context,
            TEXTDATA="This email is for activation of your account"
        )

        return status
