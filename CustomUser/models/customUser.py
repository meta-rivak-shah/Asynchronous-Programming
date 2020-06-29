from django.contrib.auth.models import AbstractBaseUser
from CommonApp.base import *
from CustomUser.Manager.customUser import CustomUserManager
from CustomUser.validations.validations import userValidations
from datetime import datetime
from dateutil.relativedelta import relativedelta


# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}/'.format(instance.id, filename )


class CustomUserModel( AbstractBaseUser, CustomModel, DeletableWrapper, IdWrapper ):
    email = models.EmailField( max_length=255, unique=True )
    active = models.BooleanField( default=False )
    user_name = models.CharField( max_length=12, null=True, blank=True )
    first_name = models.CharField( max_length=128 )
    last_name = models.CharField( max_length=128, blank=True, null=True )
    is_email_verified = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    profile_pic = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    invitation_token = models.UUIDField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey('CustomUser.CustomUserModel', related_name='%(class)s_updated_by',
                                    on_delete=models.CASCADE, null=True, blank=True)
    failed_login_attempts = models.PositiveSmallIntegerField( default=0, blank=True, null=True )
    block_timer = models.DateTimeField( null=True, blank=True )

    objects = CustomUserManager()
    validations = userValidations()

    USERNAME_FIELD = 'email'  # username of admin

    # email and password is required by default

    REQUIRED_FIELDS = ['first_name', 'last_name',]

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __int__(self):  # __unicode__ on Python 2
        return self.id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    # @property
    # def is_active(self):
    #     return self.active

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def increase_attempt_count(self):
        self.failed_login_attempts += 1
        self.save()

    def reset_attempt(self):
        self.failed_login_attempts = 0
        self.save()

    def set_timer(self):
        self.block_timer = datetime.now() + relativedelta(minutes=15)
        self.save()

    def reset_timer(self):
        self.block_timer = None
        self.save()
