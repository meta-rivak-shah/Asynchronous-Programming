from django.db import transaction
from django.shortcuts import redirect
from django.utils import timezone

from CustomUser.models import CustomUserModel, EmailConfirmationModel, LoginAuditLogModel
from CustomUser.forms import RegisterForm, LoginForm
from django.views import View
from CommonApp import stringconstant
from ApiResponse.function import *
from django.contrib.auth import authenticate, login, logout


class verify_authenticate(object):

    def __init__(self, allowed_for):
        self.allowed_for = allowed_for

    def __call__(self, func):
        def _inner(method_self, request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect('/dashboard/home')
            elif request.session.get('user', default=None):
                return redirect('/user/sign_up')
            return func(method_self, request, *args, **kwargs)
        return _inner


class AddCustomUser(View):
    # REGISTER All User
    # API user/sign_up
    @verify_authenticate(allowed_for = (stringconstant.ALL_USER,))
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = {
            stringconstant.LOGIN_FORM: LoginForm()
        }
        signup_form = RegisterForm(request.POST)
        if signup_form.is_valid():
            try:
                email_confirm = None
                user = CustomUserModel.objects.create_custom_user(signup_form)
                if user:
                    email_confirm = EmailConfirmationModel.objects.create_email_invitation_form(user)
                if email_confirm:
                    try:
                        status = email_confirm.send_email( stringconstant.ACCOUNT_ACTIVATE_MAIL, user.email )
                        if not status:
                            raise Exception
                        data['success'] = True
                        data[stringconstant.FORM] = RegisterForm()
                        return success_response(request, 'LOGIN_REGISTER_TEMPLATE', 'ACCOUNT_CREATED_WITH_MAIL', data)
                    except Exception as e:
                        data['warning'] = True
                        data[stringconstant.FORM] = RegisterForm()
                        return warning_response( request, 'LOGIN_REGISTER_TEMPLATE', 'ACCOUNT_CREATED_WITHOUT_MAIL',data )
            except ValueError:
                data[stringconstant.FORM] = signup_form
                return model_form_response(request, 'LOGIN_REGISTER_TEMPLATE', "FORM", data)

        data['form_error'] = signup_form.is_valid()
        data[stringconstant.FORM] = signup_form
        return model_form_response(request, 'LOGIN_REGISTER_TEMPLATE', "FORM", data)

    @verify_authenticate( allowed_for=(stringconstant.ALL_USER,) )
    def get(self, request, *args, **kwargs):
        data = {
            stringconstant.FORM:RegisterForm(),
            stringconstant.LOGIN_FORM:LoginForm(),
        }
        return model_form_response(request, 'LOGIN_REGISTER_TEMPLATE', "FORM", data)


# LOGIN CLASS FOR ALL USER
# API user/sign_in
class AuthenticateAccount(View):
    _FAILED_LOGIN_ATTEMPTS = 3

    @verify_authenticate(allowed_for=(stringconstant.ALL_USER,))
    def post(self, request, *args, **kwargs):
        time_now = timezone.now()
        data = {
            stringconstant.FORM: RegisterForm()
        }
        login_form = LoginForm(request.POST)
        if not login_form.is_valid():
            data['error'] = True
            data[stringconstant.LOGIN_FORM] = login_form
            return error_response(request, 'LOGIN_REGISTER_TEMPLATE', 'INVALID_DATA', data)

        audit_obj = LoginAuditLogModel.objects.create_audit_log(ip=request.META['REMOTE_ADDR'],
                                                                HTTP_ORIGIN=request.META['HTTP_ORIGIN'])
        try:
            CustomUserModel.objects.get(email__iexact=login_form.clean_email(), is_deleted=False)
        except Exception as e:
            data['error'] = True
            data[stringconstant.LOGIN_FORM] = login_form
            audit_obj.update_log(email=login_form.clean_email(), status='FAILURE', exception=str(e))
            return error_response(request, 'LOGIN_REGISTER_TEMPLATE', 'NO_EMAIL_FOUND', data)

        # check password and Email is valid credential
        try:
            user_obj = authenticate(request, username=login_form.clean_email(), password=login_form.clean_password())
            if user_obj is None:
                raise NameError('Email And Password Is Incorrect')
        except NameError as e:
            error_type = 'INACTIVE_ACCOUNT'
            custom_obj = CustomUserModel.objects.get(email__iexact=login_form.clean_email(), is_deleted=False)
            if custom_obj.active:
                error_type = 'INVALID_CREDENTIAL'
                if custom_obj.failed_login_attempts > 1:
                    error_type = 'INVALID_CREDENTIAL_WITH_LOCK_MES'

                if custom_obj.failed_login_attempts < self._FAILED_LOGIN_ATTEMPTS:
                    custom_obj.increase_attempt_count()
                elif custom_obj.failed_login_attempts == self._FAILED_LOGIN_ATTEMPTS:
                    custom_obj.increase_attempt_count()
                    custom_obj.set_timer()
                elif custom_obj.failed_login_attempts > self._FAILED_LOGIN_ATTEMPTS and custom_obj.block_timer and custom_obj.block_timer <= time_now:
                    custom_obj.reset_timer()
                    custom_obj.reset_attempt()
                elif custom_obj.failed_login_attempts > self._FAILED_LOGIN_ATTEMPTS and custom_obj.block_timer and custom_obj.block_timer >= time_now:
                    e = 'Account Lock Down For 15 Minute'
                    error_type = "ACCOUNT_LOCKED"
            audit_obj.update_log(email=login_form.clean_email(), user=custom_obj, status='FAILURE', exception=str(e))
            data['error'] = True
            data[stringconstant.LOGIN_FORM] = login_form
            return error_response(request, 'LOGIN_REGISTER_TEMPLATE', error_type, data)

        try:
            if user_obj:
                custom_obj = CustomUserModel.objects.get(email=user_obj)
                if not custom_obj.active:
                    raise NameError("Account is Inactive")
        except Exception as e:
            audit_obj.update_log(email=custom_obj.email, user=custom_obj, status='FAILURE',
                                 exception=str(e))
            data['error'] = True
            data[stringconstant.LOGIN_FORM] = login_form
            return error_response(request, 'LOGIN_REGISTER_TEMPLATE', 'INACTIVE_ACCOUNT', data)

        # print("========================================",user_obj)
        request.session['user'] = str(custom_obj.id)
        request.session.set_expiry(300)
        login(request, user_obj)
        audit_obj.update_log( email=custom_obj.email, user=custom_obj, status='SUCCESS',
                              exception='User Login Successfully')
        data['success'] = True
        return redirect('/dashboard/home')

    @verify_authenticate(allowed_for=(stringconstant.ALL_USER,))
    def get(self, request, *args, **kwargs):
        """
        :rtype: object
        """
        data = {
            stringconstant.FORM: RegisterForm(),
            stringconstant.LOGIN_FORM: LoginForm(),
        }
        # logout(request)
        return model_form_response(request, 'LOGIN_REGISTER_TEMPLATE', "FORM", data)

