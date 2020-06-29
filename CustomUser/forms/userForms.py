from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from CustomUser.models.customUser import CustomUserModel


class LoginForm( forms.Form ):
    email = forms.CharField( required=True, label='Email',
                             widget=forms.EmailInput(
                                 attrs={"placeholder": "Email"} ) )

    password = forms.CharField( required=True, label='Password',
                                widget=forms.PasswordInput(
                                    attrs={"placeholder": "Password"} ) )

    def clean_email(self):
        return self.cleaned_data.get('email')

    def clean_password(self):
        return self.cleaned_data.get('password')


class RegisterForm( forms.ModelForm ):
    password1 = CustomUserModel.validations.password1( required=True, label='Password',
                                                       widget=forms.PasswordInput(
                                                           attrs={"placeholder": "Password"} ) )
    password2 = CustomUserModel.validations.password2( required=True, label='Confirm Password',
                                                       widget=forms.PasswordInput(
                                                           attrs={"placeholder": "Confirm Password"} ) )

    first_name = CustomUserModel.validations.first_name( required=True, label='First Name', widget=forms.TextInput(
        attrs={"placeholder": "First Name"} ) )
    last_name = CustomUserModel.validations.last_name( required=True, label='Last Name',
                                                       widget=forms.TextInput(
                                                           attrs={"placeholder": "Last Name"} ) )
    email = CustomUserModel.validations.email( required=True, label='Email',
                                               widget=forms.EmailInput(
                                                   attrs={"placeholder": "Email"} ) )

    # email = CustomUserModel.validations.email(required=True)

    def clean_email(self):
        email = self.cleaned_data.get( 'email' )
        qs = CustomUserModel.objects.filter( email=email )
        if qs.exists():
            raise forms.ValidationError( "email is taken" )
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    class Meta:
        model = CustomUserModel
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class UserAdminCreationForm( forms.ModelForm ):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField( label='Password', widget=forms.PasswordInput )
    password2 = forms.CharField( label='Password confirmation', widget=forms.PasswordInput )

    class Meta:
        model = CustomUserModel
        fields = ('email', 'password1', 'password2',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get( "password1" )
        password2 = self.cleaned_data.get( "password2" )
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError( "Passwords don't match" )
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super( UserAdminCreationForm, self ).save( commit=False )
        user.created_by = user
        user.save()
        user.set_password( self.cleaned_data["password1"] )
        if commit:
            user.save()
        return user


class UserAdminChangeForm( forms.ModelForm ):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUserModel
        fields = ('email',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]