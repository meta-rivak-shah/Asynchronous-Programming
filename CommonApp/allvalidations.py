from django import forms
from django.core.validators import RegexValidator
from CommonApp import stringconstant as stringConstants


####################################################################################
#
# GENERIC VALIDATIONS
#
####################################################################################
# Allows mutiple aregex's to be validated

def customRegexValidator(min_length, max_length, regex, message, required, label, widget):
    """

    :param message:
    :param required:
    :param allow_blank:
    :param min_length:
    :param max_length:
    :type regex: object
    """
    return forms.CharField(
        validators=[RegexValidator( regex=regex, message=(message), )],
        min_length=min_length,
        max_length=max_length,
        required=required,
        label=label,
        widget=widget,
    )


def choiceValidator(choices, required=True):
    return forms.ChoiceField( choices=choices, required=required )


# ALLOWS NORMAL TEXT TO BE VALIDATED ( ADDRESS, COMMENTS )

def textValidator(min_length=1, max_length=200, required=True, label=None, widget=None, message=None):
    regex = r'^[a-zA-Z0-9][a-zA-Z0-9/,#&\s\+\.]{' + f'{min_length - 1},{max_length - 1}' + '}$'
    if message is None:
        message = stringConstants.CHARACTER_ERROR
    return customRegexValidator( min_length, max_length, regex, message, required, label, widget )


# Only Integers to be accepted as chars.
def integerValidator(min_length=1, max_length=16, allow_blank=False, required=True):
    regex = r'^[0-9]{' + f'{min_length},{max_length}' + '}$'
    message = f'{stringConstants.RANGE_ERROR}'
    return customRegexValidator( min_length, max_length, regex, message, allow_blank, required )


# Only accepts positive decimals
def decimalValidator(min_value=0.00, max_digits=16, decimal_places=2, required=True, **kwargs):
    return forms.DecimalField(
        max_digits=max_digits,
        decimal_places=decimal_places,
        required=required,
        **kwargs
    )




def uuidValidator(required=True):
    return forms.UUIDField( required=required )


####################################################################################
##
## SPECIFIC VALIDATIONS
##
####################################################################################
def personNameValidator(required=True, label=None, widget=None):
    min_length = 2
    max_length = 128
    regex = r'^[a-zA-Z][a-zA-Z\s]{' + f'{min_length - 2},{max_length - 2}' + '}[a-zA-Z]$'
    message = stringConstants.NAME_ERROR
    return customRegexValidator( min_length, max_length, regex, message, required, label, widget )


def stakeholderNameValidator(required=True, label=None, widget=None):
    min_length = 2
    max_length = 128
    regex = r'^[a-zA-Z][a-zA-Z\s&\.]{' + f'{min_length - 2},{max_length - 2}' + '}[a-zA-Z.]$'
    message = stringConstants.NAME_ERROR
    return customRegexValidator( min_length, max_length, regex, message, required, label, widget )


# def countryCodeValidator(required = True):
#     min_length = 2
#     max_length = 5
#     regex = r'^[0-9+][0-9]{' + f'{min_length-1},{max_length-1}' + '}$'
#     message = 'The given country code is invalid'
#     return customRegexValidator(min_length, max_length, regex, message, False, required)


def contactNumberValidator(required=True, max_length=10, min_length=10, label=None, widget=None):
    regex = r'^(\+\d{1, 3})?,?\s?\d{' + f'{min_length},{max_length}' + '}$'
    message = stringConstants.PHONE_NUMBER_ERROR
    return customRegexValidator( min_length, max_length, regex, message, required, label, widget )


def emailValidator(required=True, verify_unique=False, label=None, widget=None):
    if verify_unique:
        pass
        # RUN QUERY ON ALL EMAIL HERE.
    return forms.EmailField( min_length=10, required=required, label=label, widget=widget )


def designationValidator(required=True, label=None, widget=None):
    min_length = 2
    max_length = 128
    regex = r'^[A-Za-zÀ-ÖØ-öø-ÿ0-9/,#&\s+.]{1,127}$'
    message = stringConstants.DESIGNATION_ERROR,
    return customRegexValidator( min_length, max_length, regex, message, required, label, widget )


def accountNumberValidator(required=True, label=None, widget=None):
    return integerValidator( min_length=8, max_length=16, required=required, label=label, widget=widget )


def amountValidator(min_value=0.0, required=True, label=None, widget=None):
    return decimalValidator( min_value=min_value, required=required, label=label, widget=widget )


def addressValidator(allow_blank=True, required=True, label=None, widget=None):
    return textValidator(
        min_length=10,
        max_length=1024,
        message=stringConstants.ADDRESS_ERROR,
        required=required,
        label=label, widget=widget
    )


def ibanValidator(required=False, label=None, widget=None):
    regex = r'^[A-Z\d]+$'
    message = stringConstants.IBAN_ERROR
    return customRegexValidator( 0, 150, regex, message, required, label=label, widget=widget )


def swiftCodeValidator(required=False, label=None, widget=None):
    regex = r'^[A-Z\d]+$'
    message = stringConstants.SWIFT_CODE
    return customRegexValidator( 0, 150, regex, message, required, label=label, widget=widget )


def tenorValueValidator(required=True, label=None, widget=None):
    return forms.IntegerField( min_value=1, max_value=360, required=required, label=label, widget=widget )


def dateValidator(required=True, label=None, widget=None):
    return forms.DateField( required=required, label=label, widget=widget )


def datetimeValidator(required=True, label=None, widget=None):
    return forms.DateTimeField( required=required, label=label, widget=widget )


def rateValidator(required, label=None, widget=None):
    return decimalValidator( max_value=20, max_digits=4, decimal_places=2, required=required, label=label,
                             widget=widget )


def passwordValidator(required, label=None, widget=None):
    # return serializers.CharField(
    #     validators = settings.AUTH_PASSWORD_VALIDATORS,
    #     min_length = 8,
    #     max_length = 20
    # )
    min_length = 8
    max_length = 16
    regex = r'^[a-zA-Z0-9~@#^-_]{' + f'{min_length},{max_length}' + '}$'
    message = stringConstants.PASSWORD_ERROR
    return customRegexValidator( min_length, max_length, regex, message, required, label=label, widget=widget )
