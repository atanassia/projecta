# profilefrom django.contrib.auth.mixins import LoginRequiredMixin

from . import models
import django_filters
from django.db import IntegrityError


class ObjectFilter(django_filters.FilterSet):
    client = django_filters.CharFilter(field_name='client',
                                       lookup_expr='name__icontains', label='Клиент')

    address = django_filters.CharFilter(field_name='address',
                                        lookup_expr='icontains', label='Адрес')

    def __init__(self, *args, company, **kwargs):
        super(ObjectFilter, self).__init__(*args, **kwargs)
        try:
            self.filters['responsible'] = django_filters.ChoiceFilter(
                field_name='responsible',
                choices=[(item.id, item) for item in models.User.objects.filter(
                    executor=company,
                    position='Plumber',
                    is_superuser=False,
                )
                         ],
                label='Ответственный'
            )
        except IntegrityError:
            self.filters['responsible'] = []

    class Meta:
        model = models.Agreement
        fields = ['client', 'address', 'responsible']


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name',
                                           lookup_expr='icontains', label='Имя')

    last_name = django_filters.CharFilter(field_name='last_name',
                                          lookup_expr='icontains', label='Фамилия')

    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'position']


class ClientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Наименование'
    )

    class Meta:
        model = models.Client
        fields = ['name', 'inn', 'kpp']


class AgreementFilter(django_filters.FilterSet):
    client = django_filters.CharFilter(
        field_name='client',
        lookup_expr='name__icontains',
        label='Клиент'
    )
    object = django_filters.CharFilter(
        field_name='object',
        lookup_expr='address__icontains',
        label='Объект'
    )

    date_from_year = django_filters.NumberFilter(
        field_name='date_from',
        lookup_expr='year',
        label='Год начала',
    )

    date_from_month = django_filters.NumberFilter(
        field_name='date_from',
        lookup_expr='month',
        label='Месяц начала',
    )

    date_to_year = django_filters.NumberFilter(
        field_name='date_to',
        lookup_expr='year',
        label='Год конца',
    )

    date_to_month = django_filters.NumberFilter(
        field_name='date_to',
        lookup_expr='month',
        label='Месяц конца',
    )
    num_reg_certificate = django_filters.CharFilter(
        field_name='num_reg_certificate',
        lookup_expr='icontains',
        label='Регистрационный №'
    )
    license = django_filters.ChoiceFilter(
        field_name='license',
        lookup_expr='icontains',
        choices=[('', 'Все'), ('Нет лицензии', 'Нет лицензии')]
    )

    class Meta:
        model = models.Agreement
        fields = ['agreement_number', 'num_reg_certificate', 'client', 'address', 'status']


class TicketFilter(django_filters.FilterSet):
    agreement = django_filters.CharFilter(
        field_name='agreement',
        lookup_expr='agreement_number__icontains',
        label='Соглашение'
    )

    object = django_filters.CharFilter(
        field_name='agreement',
        lookup_expr='address__icontains',
        label='Объект'
    )

    execution_date_year = django_filters.NumberFilter(
        field_name='execution_date',
        lookup_expr='year',
        label='Год',
    )

    execution_date_month = django_filters.NumberFilter(
        field_name='execution_date',
        lookup_expr='month',
        label='Месяц',
    )

    def __init__(self, *args, company, **kwargs):
        super(TicketFilter, self).__init__(*args, **kwargs)
        try:
            self.filters['responsible'] = django_filters.ChoiceFilter(
                field_name='agreement',
                lookup_expr='responsible__id__iexact',
                choices=[(item.id, item) for item in models.User.objects.filter(
                    executor=company,
                    position='Plumber',
                    is_superuser=False,
                )
                         ],
                label='Ответственный'
            )
        except IntegrityError:
            self.filters['responsible'] = []

    class Meta:
        model = models.Ticket
        fields = ['agreement', 'type', 'status', 'execution_date_year', 'execution_date_month']

class ActFilter(django_filters.FilterSet):
    class Meta:
        model = models.Act
        fields = ['act_number', 'agreement', 'act_date', 'act_status',
                  'check_number', 'check_status']

class EquipmentFilter(django_filters.FilterSet):
    date_from_year = django_filters.NumberFilter(
        field_name='date_from',
        lookup_expr='year',
        label='Год начала',
    )

    date_from_month = django_filters.NumberFilter(
        field_name='date_from',
        lookup_expr='month',
        label='Месяц начала',
    )

    date_to_year = django_filters.NumberFilter(
        field_name='date_to',
        lookup_expr='year',
        label='Год конца',
    )

    date_to_month = django_filters.NumberFilter(
        field_name='date_to',
        lookup_expr='month',
        label='Месяц конца',
    )
    class Meta:
        model = models.Equipment
        fields = ['type', 'date_from_year', 'date_from_month', 'date_to_year', 'date_to_month']

class InsurancePolicyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name_insurance_company',
        lookup_expr='icontains',
        label='Наименование'
    )

    date_from_year = django_filters.NumberFilter(
        field_name='date_from',
        lookup_expr='year',
        label='Год начала',
    )

    date_from_month = django_filters.NumberFilter(
        field_name='date_from',
        lookup_expr='month',
        label='Месяц начала',
    )

    date_to_year = django_filters.NumberFilter(
        field_name='date_to',
        lookup_expr='year',
        label='Год конца',
    )

    date_to_month = django_filters.NumberFilter(
        field_name='date_to',
        lookup_expr='month',
        label='Месяц конца',
    )
    class Meta:
        model = models.Equipment
        fields = ['name', 'date_from_year', 'date_from_month', 'date_to_year', 'date_to_month']