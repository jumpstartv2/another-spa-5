from __future__ import (
    absolute_import,
    unicode_literals,
)

from django.conf import settings
from django.core.mail import send_mail


def send_email_template(subject, template, recipient, data=None):
    """
    This function sends an email using a selected template.

    Arguments:
        subject: the subject of the email
        template: the template to be used for the email
        recipient: a list of recipients the email will be sent to
        data: a dictionary to be added as context variables in the email
    """
    context = {
        'current_site': Site.objects.get_current().domain,
    }
    context.update(data)

    html_content = render_to_string(template, context)
    text_content = strip_tags(html_content)

    send_mail(
        subject=subject,
        message=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient,
        fail_silently=False,
        html_message=html_content
    )
