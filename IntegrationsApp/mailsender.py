from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from django.utils import timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from CommonApp.celery import app
from celery.utils.log import get_task_logger
from django.utils.module_loading import import_string

SENDER = settings.SES_SENDER_EMAIL
CHARSET = "UTF-8"


@app.task(name='Send Email with attachment via SES')
def async_send_email(RECIPIENT, SUBJECT, TEMPLATE_DATA, file_path, file_name, CC_RECIPIENT=None):
    """

    :param SUBJECT:
    :param TEMPLATE_DATA:
    :param file_path:
    :param file_name:
    :param CC_RECIPIENT:
    :type RECIPIENT: basestring
    """
    # check weather RECIPIENT IS string format or not
    if str == type(RECIPIENT):
        RECIPIENCELERY_BROKER_URLT = [RECIPIENT]
    else:
        # Remove the duplicate email if available
        RECIPIENT = list(set(RECIPIENT))

    if type(CC_RECIPIENT) == str:
        CC_RECIPIENT = [CC_RECIPIENT]

    if CC_RECIPIENT is None:
        CC_RECIPIENT = []

    try:
        email = EmailMessage(
            subject=SUBJECT,
            body=TEMPLATE_DATA,
            from_email=settings.SES_SENDER_EMAIL,
            to=RECIPIENT,
            cc=CC_RECIPIENT
        )
        email.content_subtype = 'html'
        email.send()
        STATUS = "Email sent!"
    except Exception as e:
        STATUS = f"ERROR : {str(e)}"


def renderEmailTemplate(TEMPLATEPATH, CONTEXT):
    template = get_template(TEMPLATEPATH)
    html = template.render(CONTEXT)
    return html


def send_email(RECIPIENT, SUBJECT, TEMPLATEPATH, CONTEXT, TEXTDATA, CC_RECIPIENT=None):
    TEMPLATE_DATA = renderEmailTemplate(TEMPLATEPATH, CONTEXT)
    return async_send_email.delay(RECIPIENT, SUBJECT, TEMPLATE_DATA, TEXTDATA, CC_RECIPIENT)


def send_email_with_attachment():
    pass
