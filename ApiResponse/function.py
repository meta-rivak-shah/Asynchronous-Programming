from django.shortcuts import render
from .keys import *
from .templateName import *

NOT_FOUND_TEMPLATE = None


def generic_response(request, template_name, responseType, main_message=None, extra_message=None, data=None):
    response = {
        'type': responseType,
        'main_message': main_message,
        'extra_message': extra_message,
    }
    if data is not None:
        response['data'] = data
    return render(request, template_name, response)


def success_response(request, template_name, key, data):
    message = SUCCESS_RESPONSES.get(key, None)
    template_name = TEMPLATES.get(template_name, NOT_FOUND_TEMPLATE)
    return generic_response(
        request,
        template_name,
        responseType="success",
        main_message=message.main_message,
        extra_message=message.extra_message,
        data=data,
    )


def error_response(request, template_name, key, data):
    message = ERROR_RESPONSES.get(key, None)
    template_name = TEMPLATES.get(template_name, NOT_FOUND_TEMPLATE)
    return generic_response(
        request,
        template_name,
        responseType="success",
        main_message=message.main_message,
        extra_message=message.extra_message,
        data=data,
    )


def warning_response(request, template_name, key, data):
    message = WARNING_RESPONSES.get(key, None)
    template_name = TEMPLATES.get(template_name, NOT_FOUND_TEMPLATE)
    return generic_response(
        request,
        template_name,
        responseType="success",
        main_message=message.main_message,
        extra_message=message.extra_message,
        data=data,
    )


def info_response(request, template_name, key, data):
    message = INFO_RESPONSES.get(key, None)
    template_name = TEMPLATES.get(template_name, NOT_FOUND_TEMPLATE)
    return generic_response(
        request,
        template_name,
        responseType="success",
        main_message=message.main_message,
        extra_message=message.extra_message,
        data=data,
    )


def model_form_response(request, template_name, key, data):
    message = MODEL_RESPONSES.get(key, None)
    template_name = TEMPLATES.get(template_name, NOT_FOUND_TEMPLATE)
    return generic_response(
        request,
        template_name,
        responseType="success",
        main_message=message.main_message,
        extra_message=message.extra_message,
        data=data,
    )
