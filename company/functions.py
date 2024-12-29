from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_company_creation_email(company):

    subject = f"New Company Created: {company.company_name}"
    html_message = render_to_string(
        'emails/company_creation_email.html',
        {
            'owner_first_name': company.owner.first_name,
            'company_name': company.company_name,
            'description': company.description,
            'number_of_employees': company.number_of_employees,
        }
    )

    recipient_email = company.owner.email
    send_mail(
        subject,
        '',
        settings.EMAIL_HOST_USER,
        [recipient_email],
        html_message=html_message
    )