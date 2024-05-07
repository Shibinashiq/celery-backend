from celery import shared_task
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


@shared_task(bind=True)

def test_func(self):
    for i in range(10):
        print(i)
    return "done"

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
import os


@shared_task(bind=True)
def celery_task(self,superuser_email):
    from  User.models import Order
    print("hiiiiiiiiiiiiii")
    orders = Order.objects.all()  
    print(orders)
    print(superuser_email)

    context = {'orders': orders}  

    email_content = render_to_string('invoice.html', context)

    sender_email = os.environ.get('SENDER_EMAIL')
    plain_message=strip_tags(email_content)
    message=EmailMultiAlternatives(
        subject=    'Subject of the email',
        body=plain_message,
        from_email=sender_email,
        to=[superuser_email]
    )
    message.attach_alternative(email_content, "text/html")
    message.send()