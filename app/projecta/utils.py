import datetime
import json
import string
import random
from time import sleep

from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from project_a.context import context


def get_last_day():
    current_date = datetime.datetime.utcnow()
    pre_last_date = current_date.replace(day=28)
    next_month = pre_last_date + datetime.timedelta(days=4)
    last_date = next_month - datetime.timedelta(days=next_month.day)
    return last_date.date()


def load_request_data(request):
    request_data = json.loads(request.body.decode('utf-8'))
    try:
        request_data.pop('csrfmiddlewaretoken')
    except KeyError:
        pass
    return request_data


def order_tickets(tickets):
    ordering = {
        'Инцидент': 1,
        'Ремонт': 2,
    }

    return sorted(tickets, key=lambda x: ordering.get(x.type) or 3)


def gen_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(random.choice(alphabet) for i in range(12))
    return password


def send_email(user, created_user, password):
    html_version = 'emails/create_user_email.html'
    html_message = render_to_string(
        html_version,
        {
            'username': created_user,
            'password': password
        }
    )

    message = EmailMessage(
        'Регистрация',
        html_message,
        context.email_config['user'],
        [user, context.email_config['user']]
    )
    message.content_subtype = 'html'  # this is required because there is no plain text email version
    message.send()


def is_delete_message(title):
    return JsonResponse({
            'message': [f'{title} удален(а).'],
            'status': 'danger'
        },
        status=403
    )


def is_active_message(title):
        return JsonResponse({
            'message': [f'{title} неактивен(вна).'],
            'status': 'warning'
        },
        status=403
    )





