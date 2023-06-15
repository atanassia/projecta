from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError

from projecta import models
from projecta.models import User


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Create default groups"

    def create_permission(self, codename, name, content_type):
        Permission.objects.create(
            codename=codename,
            name=name,
            content_type=content_type,
        )

    def handle(self, *args, **options):
        groups = {
            'Director': [],
            'Engineer': [],
            'Accountant': [
                'view_user',
                'view_ticket',
                'view_act',
                'view_agreement',
                'view_client',
                'view_executor',
                'view_license',
                'view_insurancepolicy',
                'add_act',
                'change_act',
                'change_client',
                'change_ticket',

                'add_ticket',
                'add_clientcontact',
                'add_act',

                'delete_clientcontact',
                'change_clientcontact',
                'change_client_status_field',
                'change_agreement_status_field',
                'change_user_status_field',
                'change_act_status_field',
                'change_ticket_status_field',
                'can_create_excel_file'
            ],
            'Plumber': [
                'change_ticket_status_field',
                'change_agreement_status_field',
                'change_act_status_field',
                'view_ticket',
                'add_ticket',
                'view_executor',
                'view_license'
            ]
        }
        perms = [
            {'codename': 'change_ticket_status_field',
             'name': 'Can Change Ticket Status',
             'content_type': ContentType.objects.get_for_model(models.Ticket)},
            {'codename': 'change_client_status_field',
             'name': 'Can Change Client Status',
             'content_type': ContentType.objects.get_for_model(models.Client)},
            {'codename': 'change_agreement_status_field',
             'name': 'Can Change Agreement Status',
             'content_type': ContentType.objects.get_for_model(models.Agreement)},
            {'codename': 'change_user_status_field',
             'name': 'Can Change Worker Status',
             'content_type': ContentType.objects.get_for_model(models.User)},
            {'codename': 'change_act_status_field',
             'name': 'Can Change Act Status',
             'content_type': ContentType.objects.get_for_model(models.Act)},
            {'codename': 'can_create_excel_file',
             'name': 'Can Create Excel File',
             'content_type': ContentType.objects.get_for_model(models.User)},
        ]
        try:
            Group.objects.all().delete()
            print('Deleted')
            for perm in perms:      
                try:
                    self.create_permission(**perm)
                except IntegrityError:
                    pass

            for group in groups:
                grp, created = Group.objects.get_or_create(name=group)
                if groups[group]:
                    grp.permissions.set(Permission.objects.filter(codename__in=groups[group]))
                else:
                    grp.permissions.set(Permission.objects.all())

            print('Groups are created')

            for user in User.objects.all():
                user.groups.add(Group.objects.get(name=user.position))

            print('Roles was set')
        except IntegrityError:
            print('Something errors')
