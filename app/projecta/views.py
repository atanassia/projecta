import datetime
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import utils
from . import forms, models
from . import filters
import re


# MAIN VIEWS
# ----------------------------------------------------------------------


@login_required
@permission_required('projecta.view_client')
def client_view(request) -> render:
    """
        Renders the clients page
    """
    company = request.user.executor
    clients_qs = company.clients.filter(is_active=True, is_delete=False)
    # making a query set from list of clients

    client_filter = filters.ClientFilter
    client_form = forms.ClientForm()
    chosen_filters = None
    # applying filter to the clients
    if request.method == 'POST':
        clients_qs = client_filter(request.POST, clients_qs).qs
        chosen_filters = dict(request.POST)
        chosen_filters.pop('csrfmiddlewaretoken')

    return render(request, 'projecta/clients.html', context={
        'clients': clients_qs,
        'filter': client_filter,
        'client_form': client_form,
        'chosen_filters': chosen_filters
    })

@login_required
@permission_required('projecta.view_user')
def worker_view(request) -> render:
    """
        Renders the workers page
    """
    # Getting the current request company
    company = request.user.executor
    worker_filter = filters.UserFilter
    worker_form = forms.UserForm
    workers = company.workers.filter(is_superuser=False, is_sys_user=False)
    chosen_filters = None

    if request.method == 'POST':
        workers = worker_filter(request.POST, workers).qs
        chosen_filters = dict(request.POST)
        chosen_filters.pop('csrfmiddlewaretoken')

    return render(request, 'projecta/workers.html', context={
        'workers': workers,
        'filter': worker_filter,
        'form': worker_form,
        'chosen_filters': chosen_filters
    })

@login_required
@permission_required('projecta.view_ticket')
def ticket_view(request) -> render:
    """
        Renders the tickets page
    """
    company = request.user.executor

    ticket_filter = filters.TicketFilter(company=company)
    ticket_form = forms.TicketForm(company=company)

    tickets_qs = company.tickets.filter(is_active=True)
    
    chosen_filters = None

    if request.method == 'POST':
        tickets_qs = filters.TicketFilter(
            data=request.POST,
            company=company,
            queryset=tickets_qs
        ).qs
        chosen_filters = dict(request.POST)
        chosen_filters.pop('csrfmiddlewaretoken')

    tickets_qs = utils.order_tickets(tickets_qs)
    return render(request, 'projecta/tickets.html', context={
        'tickets': tickets_qs,
        'filter': ticket_filter,
        'ticket_form': ticket_form,
        'chosen_filters': chosen_filters
    })

@login_required
@permission_required('projecta.view_act')
def act_view(request) -> render:
    """
        Renders the acts page
    """
    company = request.user.executor
    act_filter = filters.ActFilter
    act_form = forms.ActForm(company=company)
    acts_qs = company.acts.filter(is_active=True)
    chosen_filters = None
    if request.method == 'POST':
        acts_qs = filters.ActFilter(
            data=request.POST,
            queryset=acts_qs
        ).qs
        chosen_filters = dict(request.POST)
        chosen_filters.pop('csrfmiddlewaretoken')

    return render(request, 'projecta/acts.html', context={
        'acts': acts_qs,
        'filter': act_filter,
        'form': act_form,
        'chosen_filters': chosen_filters
    })

@login_required
@permission_required('projecta.view_agreement')
def agreement_view(request) -> render:
    """
        Renders the agreements page
    """
    company = request.user.executor
    agreements = company.agreements.filter(is_active=True, is_delete=False)

    agreement_filter = filters.AgreementFilter
    agreement_form = forms.AgreementForm(company=company)
    chosen_filters = None

    if request.method == 'POST':
        agreements = agreement_filter(request.POST, agreements).qs
        chosen_filters = dict(request.POST)
        chosen_filters.pop('csrfmiddlewaretoken')

    agreements = sorted(list(agreements),key=lambda s:list(map(lambda x:int(x) if x.isdigit() else x,re.split(r'(\d+)',s.agreement_number)[1:])))
    return render(request, 'projecta/agreements.html', context={
        'agreements': agreements,
        'filter': agreement_filter,
        'agreement_form': agreement_form,
        'chosen_filters': chosen_filters
    })

@login_required
@permission_required('projecta.change_agreement')
def agreement_update_view(request, pk):
    company = request.user.executor
    agreement = models.Agreement.objects.get(pk=pk)
    update_form = forms.AgreementUpdateForm(company=company, initial=agreement.serialize(), agreement=agreement)
    if request.method == 'POST':
        request_data = dict(request.POST)
        request_data.pop('csrfmiddlewaretoken')
        for field in request_data:
            request_data[field] = request_data[field][0]
        request_data['responsible'] = models.User.objects.get(pk=request_data['responsible'])
        try:
            license = company.licenses.get(license=request_data['license'])
            request_data['class_danger'] = license.class_danger
        except ObjectDoesNotExist:
            request_data['class_danger'] = 'Нет класса'
        
        request_data['is_active'] = True if 'is_active' in request_data else False
        
        try:
            models.Agreement.objects.filter(pk=pk).update(**request_data)
            return HttpResponseRedirect(agreement.get_absolute_url())
        except ValidationError as e:
            return render(request, 'projecta/agreement_update.html', context={
                'form': update_form,
                'errors': e
            })
    else:
        return render(request, 'projecta/agreement_update.html', context={
            'form': update_form,
            'agreement': agreement
        })

@login_required
def main_view(request):
    return render(request, 'projecta/main.html')

@login_required
@permission_required('projecta.view_executor')
def executor_detail_view(request):
    company = request.user.executor
    return render(request, 'projecta/executor_detail.html', context={
        'company': company
    })

@login_required
@permission_required('projecta.change_executor')
def executor_update_view(request):
    company = request.user.executor
    update_form = forms.ExecutorForm(initial=company.serialize())
    if request.method == 'POST':
        request_data = dict(request.POST)
        request_data.pop('csrfmiddlewaretoken')
        for field in request_data:
            request_data[field] = request_data[field][0]
        models.Executor.objects.filter(pk=company.pk).update(**request_data)
        return HttpResponseRedirect(reverse('projecta:company'))

    return render(request, 'projecta/company_update.html', context={
        'company': company,
        'form': update_form
    })

@login_required
def add_equipment_photo_view(request, pk):
    message = ''
    company = request.user.executor
    if request.method == 'POST':
        ticket = models.Ticket.objects.get(pk=pk)
        equip_photo_form = forms.EquipmentPhotoForm(request.POST, request.FILES)
        files = request.FILES.getlist('photo')
        if all(str(photo).lower().endswith(('.jpg', '.png', '.jpeg')) for photo in files):
            if equip_photo_form.is_valid():
                for photo in files:
                    photo.name = f'{request.user} - {company} - {datetime.datetime.utcnow()}.jpg'
                    file = models.EquipmentPhoto(
                        photo=photo,
                        ticket=ticket,
                        author=request.user,
                        executor=request.user.executor
                    )
                    file.save()

            return HttpResponseRedirect(reverse('projecta:ticket_detail', kwargs={'pk': pk}))
        else:
            message = 'Отправьте фото в формате png, jpeg, jpg'
    form = forms.EquipmentPhotoForm
    return render(
        request, 'projecta/add_equipment_photo.html',
        context={
            'form': form,
            'ticket_id': pk,
            'message': message
        }
    )

@login_required
def equipment_view(request):
    company = request.user.executor
    equipment = company.equipment.all()

    equip_filter = filters.EquipmentFilter()
    equipment_form = forms.EquipmentForm(company=company)
    chosen_filters = None
    if request.method == 'POST':
        chosen_filters = dict(request.POST)
        chosen_filters.pop('csrfmiddlewaretoken')
    return render(request, 'projecta/equipment.html', context={
        'equipment': equipment,
        'filter': equip_filter,
        'chosen_filters': chosen_filters,
        'equipment_form': equipment_form
    })

@login_required
def insurance_policy_view(request):
    company = request.user.executor
    insurance_policy = company.insurances.all()
    policy_filter = filters.InsurancePolicyFilter()
    policy_form = forms.InsurancePolicyForm(company=company)
    chosen_filters = None
    if request.method == 'POST':
        insurance_policy = filters.InsurancePolicyFilter(
            data=request.POST,
            queryset=insurance_policy
        ).qs
        chosen_filters = dict(request.POST)
        chosen_filters.pop('csrfmiddlewaretoken')
    return render(request, 'projecta/insurance_policies.html', context={
        'policy': insurance_policy,
        'filter': policy_filter,
        'chosen_filters': chosen_filters,
        'policy_form': policy_form
    })

# SIGN IN VIEWS
# ----------------------------------------------------------------------
def login_view(request) -> render or HttpResponseRedirect:
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("projecta:main"))
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("projecta:main"))
        else:
            return render(request, "projecta/login.html", {
                "message": "Пользователь с такой электронной почтой или паролем не найден."
            })
    else:
        return render(request, 'projecta/login.html')


@login_required
def logout_view(request) -> HttpResponseRedirect:
    logout(request)
    return HttpResponseRedirect(reverse('projecta:login'))


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('projecta:main'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {
        'form': form
    })
