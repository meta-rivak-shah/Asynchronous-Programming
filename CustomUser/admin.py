from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import  UserAdmin as BaseUserAdmin
from CustomUser.models import  CustomUserModel, EmailConfirmationModel, LoginAuditLogModel
from CustomUser.forms import UserAdminChangeForm, UserAdminCreationForm

class CustomUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin','id')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','profile_pic')}),
        ('Permissions', {'fields': ('admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','first_name','last_name','profile_pic')}
         ),
    )
    search_fields = ('email','id')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CustomUserModel, CustomUserAdmin)
admin.site.register(EmailConfirmationModel)
admin.site.register(LoginAuditLogModel)
