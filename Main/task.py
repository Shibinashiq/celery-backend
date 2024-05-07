from celery import shared_task
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from celery import shared_task
from django.template.loader import render_to_string
import os

@shared_task(bind=True)
def celery_task(self,superuser_email):
    from  User.models import OrderItem
    orders = OrderItem.objects.all()  
    # print(orders)
    # print(superuser_email)
    
    context = {'orders': orders}  

    email_content = render_to_string('invoice.html', context=context)
    subject="Total summary of Lacco Product"
    sender_email = os.environ.get('SENDER_EMAIL')
    plain_message=strip_tags(email_content)
    message=EmailMultiAlternatives(
        subject=    subject,
        body=plain_message,
        from_email=sender_email,
        to=[superuser_email]
    )
    message.attach_alternative(email_content, "text/html")
    message.send()