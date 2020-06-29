# Create your views here.
from django.shortcuts import redirect
from CustomUser.models import CustomUserModel
from Dashboard.forms import PostForm
from Dashboard.models import PostModel
from django.views import View
from CommonApp import stringconstant
from ApiResponse.function import *
from django.contrib.auth import logout


class verify_user_login(object):

    def __init__(self, allowed_for):
        self.allowed_for = allowed_for

    def __call__(self, func):
        def _inner(method_self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/user/sign_up')
            elif request.session.get('user', default=None) is None:
                return redirect('/user/sign_up')
            try:
                # session_obj = Session.objects.get( session_key=request.user.logged_in_user.session_key )
                # session_obj.expire_date = session_obj.expire_date + timedelta( minutes=5 )
                # session_obj.save()
                request.session.set_expiry(300)
                user_id = request.session.get('user')
                custom_user = CustomUserModel.objects.get(id=user_id)
            except ValueError:
                return redirect('/user/sign_in')
            return func(method_self, request, custom_user, *args, **kwargs)
        return _inner


class DashBoardDetails(View):
    @verify_user_login(allowed_for=(stringconstant.ALL_USER,))
    def get(self, request, user_obj, *args, **kwargs):
        custom_obj = CustomUserModel.objects.filter(is_deleted=False)
        ids = custom_obj.values_list('id', flat=True)
        postQuery = PostModel.objects.filter(user_id__in=ids, is_deleted=False).order_by('-created_on')
        data = {
            'success': False,
            'name': user_obj.get_full_name(),
            'home':True,
            'post':postQuery
        }
        return success_response(request, 'USER_DASHBOARD_TEMPLATE', 'WELCOME_USER', data)


class PostSomething(View):
    @verify_user_login(allowed_for=(stringconstant.ALL_USER,))
    def get(self, request, user_obj, *args, **kwargs):
        """
        :rtype: object
        """
        data = {
            'name': user_obj.get_full_name(),
            'post': True,
            'type': '',
        }

        return model_form_response( request, 'USER_POST_TEMPLATE', "FORM", data)

    @verify_user_login( allowed_for=(stringconstant.ALL_USER,) )
    def post(self, request, user_obj, *args, **kwargs):
        """
        :rtype: object
        """
        data = {
            'name': user_obj.get_full_name(),
            'post': True,
            'error': False,
        }
        post_form = PostForm(request.POST)
        my_file = request.FILES.get('post_img',None)
        if not post_form.is_valid():
            data['error'] = True
            data['comment'] = post_form.cleaned_data.get('post_text', '')
            data['type'] = post_form.cleaned_data.get('post_type', '')
            return error_response(request, 'USER_POST_TEMPLATE', 'REQUIRED_DATA', data)
        if my_file:
            file_extensions = ['png', 'jpg', 'jpeg']
            if my_file.name.split('.')[1] not in file_extensions:
                data['error'] = True
                data['comment'] = post_form.cleaned_data.get('post_text', '')
                data['type'] = post_form.cleaned_data.get('post_type', '')
                return error_response(request, 'USER_POST_TEMPLATE', 'INVALID_FILE', data)
        post_obj = PostModel.objects.create_form_request(post_form, my_file, user_obj)
        if not post_obj:
            data['error'] = True
            data['comment'] = post_form.cleaned_data.get( 'post_text', '')
            data['type'] = post_form.cleaned_data.get( 'post_type', '')
            return error_response( request, 'USER_POST_TEMPLATE', 'RETRY', data)
        data['success'] = True
        data['comment'] = ''
        data['type'] = ''
        return success_response(request, 'USER_POST_TEMPLATE', "POST_CREATED", data)


class LogoutYourAccount(View):
    @verify_user_login(allowed_for=(stringconstant.ALL_USER,) )
    def get(self, request, *args, **kwargs):
        """
        :rtype: object
        """
        logout(request)
        return redirect("/user/sign_in")
