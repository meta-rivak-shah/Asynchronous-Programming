from django.contrib.auth.models import BaseUserManager
from uuid import uuid4
from random import randint


def get_user_id():
    """

       :rtype: basestring
    """
    value = randint(3,5)
    return str( uuid4().int )[:value]


def get_invitation_token():
    """

    :rtype: object
    """
    return uuid4()


def get_random_profile():
    """

       :rtype:  basestring path
    """
    value = randint(1, 16)
    local_path = 'defaults/h'+str(value)+'.png'
    return local_path


class CustomUserManager( BaseUserManager ):
    def create_user(self, email, password):
        if not email:
            raise ValueError( "email is required" )
        if not password:
            raise ValueError( "password is required" )
        email = self.normalize_email( email )
        user = self.model(
            email=email,
            password=password,
        )
        user_id = get_user_id()
        user.user_name = user_id
        user.set_password( password )
        user.created_by = user
        user.profile_pic = get_random_profile()
        user.invitation_token = get_invitation_token()
        user.save( using=self._db )
        return user


    def crete_adminuser(self, email, password=None):
        user = self.create_user(
            email,
            password
        )
        user.created_by = user
        user.admin = True
        user.is_email_verified = True
        user.save( using=self._db )
        return user


    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(
            email,
            password
        )
        user.user_name = user.first_name.upper() + "" + user.user_name
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.admin = True
        user.staff = True
        user.is_email_verified = True
        user.save( using=self._db )
        return user

    def create_custom_user(self, user_data):
        user = self.create_user(
            user_data.cleaned_data.get( 'email' ),
            user_data.cleaned_data.get( 'password1' )
        )
        user.first_name = user_data.cleaned_data.get( "first_name" )
        user.last_name = user_data.cleaned_data.get( "last_name" )
        user.is_active = False
        user.admin = False
        user.staff = False
        user.user_name = user.first_name.upper() + "" + user.user_name
        user.is_email_verified = False
        user.save( using=self._db )
        return user
