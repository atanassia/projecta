import os
import threading
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import JsonResponse, HttpResponse, FileResponse
from project_a.settings import MEDIA_ROOT
from . import models, utils
from . import forms
from .utils import load_request_data, send_email, gen_password, is_delete_message, is_active_message
from .xlsx_creator import CreatorXLSX

@login_required
@permission_required('projecta.add_client')
def create_client(request):
    if request.method == 'POST':
        request_data = load_request_data(request)

        client_form = forms.ClientForm(request_data)
        if client_form.is_valid():
            request_data['executor'] = request.user.executor
            request_data['author'] = request.user
            try:
                client = models.Client(**request_data)
                client.save()

                return JsonResponse(
                    {
                        'message': 'Клиент добавлен.',
                        'status': 'success',
                        'id': client.pk
                    },
                    status=201
                )
            except ValidationError:
                return JsonResponse({'message': 'Что-то пошло не так', 'status': 'error'}, 404)
        else:
            return JsonResponse(
                {
                    'message': [error[1] for error in list(client_form.errors.get_context().get('errors'))],
                    'status': 'warning'
                },
                status=403)

@login_required
@permission_required('projecta.add_agreement')
def create_agreement(request):
    """
    Accepts the post agreement request -> validates data and saves to the database
    """
    company = request.user.executor
    if request.method == 'POST':
        request_data = load_request_data(request)

        request_data['client'] = company.clients.get(id=request_data['client'])

        if request_data['client'].is_delete:
            return is_delete_message("Клиент")
        elif not request_data['client'].is_active:
            return is_active_message("Клиент")
        
        if request_data['responsible']:
            request_data['responsible'] = models.User.objects.get(id=request_data['responsible'])
        else:
            request_data['responsible'] = None

        request_data['executor'] = company
        request_data['author'] = request.user
        print(request_data)
        
        if not request_data['date_reg_certificate']:
            request_data['date_reg_certificate'] = '1970-01-01'
        try:
            license = company.licenses.get(license=request_data['license'])
            request_data['class_danger'] = license.class_danger
        except ObjectDoesNotExist:
            pass
        
        try:
            agreement = models.Agreement(**request_data)
            agreement.save()
        except IntegrityError:
            return JsonResponse({
                'message': ['Договор с данным номером или сертификатом уже существует.'],
                'status': 'warning',
            },status=403)
        except ValidationError:
            return JsonResponse(
                {'message': ['Не указана дата.'], 'status': 'info'},status=403)
        return JsonResponse(
            {
                'message': 'Договор добавлен.',
                'status': 'success',
                'id': agreement.pk
            },
            status=201
        )

@login_required
@permission_required('projecta.add_act')
def create_act(request):
    company = request.user.executor
    if request.method == 'POST':
        request_data = load_request_data(request)
        try:
            agreement = request_data['agreement'] = company.agreements.get(
                id=request_data['agreement']
            )

            if agreement.client.is_delete:
                return is_delete_message("Клиент")
            elif agreement.is_delete:
                return is_delete_message("Договор")
            else:
                if agreement.client.is_active:
                    if agreement.is_active:
                        if agreement.status not in ('Б/С', 'У клиента', 'Подписан'):
                            return JsonResponse(
                                {
                                    'message': [f'Данный договор имеет статус {agreement.status}, к нему нельзя добавить акт'],
                                    'status': 'warning'
                                },
                                status=403
                            )
                    else:
                        return is_active_message("Договор")
                else:
                    return is_active_message("Клиент договора")

        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': ['Данного договора не существует.'], 'status': 'warning'},
                status=403
            )

        request_data['author'] = request.user
        request_data['executor'] = company
        try:
            act = models.Act(**request_data)
            act.save()
            return JsonResponse(
                {
                    'message': ['Акт добавлен.'],
                    'status': 'success',
                    'id': act.pk
                },
                status=201
            )
        except IntegrityError:
            return JsonResponse(
                {'message': ['Данный номер акта уже существует.'], 'status': 'danger'},
                status=403
            )
        except ValidationError as e:
            return JsonResponse(
                {'message': e.messages, 'status': 'danger'},
                status=403
            )

@login_required
@permission_required('projecta.add_ticket')
def create_ticket(request):
    company = request.user.executor
    if request.method == 'POST':
        request_data = load_request_data(request)

        request_data['author'] = request.user
        request_data['executor'] = company
        try:
            agreement = request_data['agreement'] = company.agreements.get(
                id=request_data['agreement']
            )

            if agreement.client.is_delete:
                return is_delete_message("Клиент")
            elif agreement.is_delete:
                return is_delete_message("Договор")
            else:
                if agreement.client.is_active:
                    if agreement.is_active:
                        if agreement.status not in ('Б/С', 'У клиента', 'Подписан', 'ЭДО'):
                            return JsonResponse(
                                {
                                    'message': [f'Данный договор имеет статус {agreement.status}, к нему нельзя добавить заявку'],
                                    'status': 'warning'
                                },
                                status=403
                            )
                    else:
                        return is_active_message("Договор")
                else:
                    return is_active_message("Клиент")
            
            request_data['execution_date'] = (request_data.get('execution_date') or utils.get_last_day())
            ticket = models.Ticket(**request_data)
            ticket.save()
            return JsonResponse(
                {
                    'message': ['Заявка добавлена'],
                    'status': 'success',
                    'id': ticket.pk
                },
                status=201
            )
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': ['Данному договору нельзя добавить соглашение.'], 'status': 'danger'},
                status=403
            )

@login_required
@permission_required('projecta.add_clientcontact')
def create_contacts(request):
    if request.method == 'POST':
        request_data = load_request_data(request)
        client = models.Client.objects.get(id=request_data.pop('client'))
        if not client.is_delete:
            if client.is_active:
                contact_form = forms.ClientContactForm(request_data)
                if contact_form.is_valid():
                    try:
                        contacts = models.ClientContact(**request_data, client=client)
                        contacts.save()
                        return JsonResponse(
                            {
                                'message': ['Контакт добавлен.'],
                                'status': 'success',
                                'id': contacts.pk
                            },
                            status=201
                        )
                    except IntegrityError:
                        return JsonResponse(
                            {
                                'message': ['Что-то пошло не так, попробуйте снова.'],
                                'status': 'warning'
                            },
                            status=403
                        )
                else:
                    return JsonResponse(
                        {
                            'message': [error[1] for error in
                                        list(contact_form.errors.get_context().get('errors'))],
                            'status': 'warning'
                        },
                        status=403)
            else:
                return is_active_message("Клиент")
        else:
            return is_delete_message("Клиент")

@login_required
@permission_required('projecta.add_equipment')
def create_equipment(request):
    company = request.user.executor
    if request.method == 'POST':
        request_data = load_request_data(request)
        try:
            request_data['agreement'] = company.agreements.get(
                id=request_data.pop('agreement'),
                status__in=('Б/С', 'У клиента', 'Подписан', 'ЭДО')
            )
        except ObjectDoesNotExist:
            return JsonResponse(
                {'message': ['Такого договора не существует.'], 'status': 'warning'},
                status=403
            )
        
        if request_data['agreement'].client.is_delete:
            return is_delete_message("Клиент")
        elif request_data['agreement'].is_delete:
            return is_delete_message("Договор")
        else:    
            if request_data['agreement'].client.is_active:
                if request_data['agreement'].is_active:
                    try:
                        request_data['executor'] = company
                        equip = models.Equipment(**request_data)
                        equip.save()
                        return JsonResponse(
                            {
                                'message': ['Оборудование добавлено.'],
                                'status': 'success',
                                'id': equip.pk
                            },
                            status=201
                        )
                    except IntegrityError as e:
                        print(e.message)
                        return JsonResponse(
                            {'message': ['Данное оборудование уже существует.'], 'status': 'warning'},
                            status=403
                        )
                else:
                    return is_active_message("Договор")
            else:
                return is_active_message("Клиент")

@login_required
@permission_required('projecta.add_user')
def create_user(request):
    company = request.user.executor
    if request.method == 'POST':
        request_data = load_request_data(request)
        request_data['executor'] = company
        user_form = forms.UserForm(request_data)
        if user_form.is_valid():
            try:
                with transaction.atomic():
                    user = models.User(**request_data)
                    # psswrd = gen_password()
                    psswrd = '1234'
                    user.set_password(psswrd)
                    user.save()
                    # threading.Thread(target=send_email, kwargs={
                    #     'user': request.user.email,
                    #     'created_user': user.email,
                    #     'password': psswrd
                    # }).start()
                    user.groups.add(Group.objects.get(name=user.position))
                return JsonResponse(
                    {
                        'message': ['Сотрудник успешно добавлен'],
                        'status': 'success',
                        'id': user.pk
                    },
                    status=201
                )
            except IntegrityError:
                return JsonResponse(
                    {
                        'message': [error[1] for error in list(user_form.errors.get_context().get('errors'))],
                        'status': 'warning'
                    },
                    status=403)
        else:
            return JsonResponse(
                {
                    'message': [error[1] for error in list(user_form.errors.get_context().get('errors'))],
                    'status': 'warning'
                },
                status=403)

@login_required
@permission_required('projecta.add_license')
def create_license(request):
    company = request.user.executor
    if request.method == 'POST':
        request_data = load_request_data(request)
        request_data['executor'] = company
        try:
            license = models.License.objects.create(**request_data)
            return JsonResponse(data={
                'message': 'Лицензия успещно добавлена.',
                'status': 'success',
                'id': license.pk
            }, status=201)
        except IntegrityError:
            return JsonResponse(data={
                'message': 'Что-то пошло не так.',
                'status': 'warning'
            }, status=400)

@login_required
@permission_required('projecta.add_insurance_policy')
def create_insurance_policy(request):
    company = request.user.executor
    if request.method == 'POST':
        request_data = load_request_data(request)
        request_data['executor'] = company
        request_data['agreement'] = company.agreements.get(id=request_data['agreement'])
        
        if request_data['agreement'].client.is_delete:
            return is_delete_message("Клиент")
        elif request_data['agreement'].is_delete:
            return is_delete_message("Договор")
        else:
            if request_data['agreement'].client.is_active:
                if request_data['agreement'].is_active:
                    try:
                        insurance_policy = models.InsurancePolicy.objects.create(**request_data)
                        return JsonResponse(data={
                            'message': 'Страховой полис успешно добавлен.',
                            'status': 'success',
                            'id': insurance_policy.pk
                        }, status=201)
                    except IntegrityError:
                        return JsonResponse(data={
                            'message': 'Что-то пошло не так.',
                            'status': 'warning'
                        }, status=400)
                else:
                    return is_active_message("Договор")
            else:
                return is_active_message("Клиент")

@login_required
def delete_equipment_photo(request, pk):
    if request.method == 'DELETE':
        try:
            photo = models.EquipmentPhoto.objects.get(pk=pk)
            os.remove(os.path.join(MEDIA_ROOT, str(photo.photo)))
            photo.delete()
            return HttpResponse(status=200)
        except models.EquipmentPhoto.DoesNotExist:
            return HttpResponse(status=404)

@login_required
@permission_required('projecta.update_client_is_delete')
def change_client_is_delete(request, pk):
    if request.method == 'PUT':
        client = models.Client.objects.get(pk=pk)
        client.is_delete = True
        client.save()

        return JsonResponse(
            {
                'message': ['Удаление клиента', 'Клиент успешно удален.'],
                'status': 'success'
            },
            status=202
        )

@login_required
@permission_required('projecta.update_agreement_is_delete')
def change_agreement_is_delete(request, pk):
    if request.method == 'PUT':
        agreement = models.Agreement.objects.get(pk=pk)
        agreement.is_delete = True
        agreement.save()

        return JsonResponse(
            {
                'message': ['Удаление договора', 'Договор успешно удален.'],
                'status': 'success'
            },
            status=202
        )

@login_required
@permission_required('projecta.change_ticket_status_field')
def change_ticket_status(request, pk):
    if request.method == 'PUT':
        request_data = load_request_data(request)
        try:
            ticket = models.Ticket.objects.get(pk=pk)
        except models.Ticket.DoesNotExist:
            return JsonResponse(
                {
                    'message': ['Статус заявки', 'Данной заявки не существует'],
                    'status': 'danger'
                },
                status=403
            )
        
        if ticket.is_active:
            new_status = request_data.get('status')
            if new_status in [status[0] for status in models.Ticket.STATUS_CHOICES]:
                ticket.status = new_status
                ticket.save()
                return JsonResponse(
                    {
                        'message': ['Статус заявки', 'Статус успешно изменён.'],
                        'status': 'success'
                    },
                    status=202
                )
            return JsonResponse(
                {
                    'message': ['Статус заявки', 'Данный статус не доступен'],
                    'status': 'danger'
                },
                status=403
            )
        else:
            return is_active_message("Заявка")

@login_required
@permission_required('projecta.change_ticket_status_field')
def change_ticket_type(request, pk):
    if request.method == 'PUT':
        request_data = load_request_data(request)
        ticket = models.Ticket.objects.get(pk=pk)
        if ticket.is_active:
            new_type = request_data.get('status')
            if new_type in [status[0] for status in models.Ticket.TYPE_CHOICES]:
                ticket.type = new_type
                ticket.save()
                return JsonResponse(
                    {
                        'message': ['Тип заявки', 'Тип успешно изменён.'],
                        'status': 'success'
                    },
                    status=202
                )
            return JsonResponse(
                {
                    'message': ['Тип заявки', 'Данный тип не доступен'],
                    'status': 'danger'
                },
                status=403
            )
        else:
            return is_active_message("Заявка")

@login_required
@permission_required('projecta.change_ticket_status_field')
def change_ticket_comment(request, pk):
    if request.method == 'PUT':
        request_data = load_request_data(request)
        ticket = models.Ticket.objects.get(pk=pk)
        if ticket.is_active:
            new_comment = request_data.get('status')
            ticket.comment = new_comment
            ticket.save()
            return JsonResponse(
                {
                    'message': ['Комментарий', 'Комментрий успешно изменён.'],
                    'status': 'success'
                },
                status=202
            )
        else:
            return is_active_message("Заявка")

@login_required
def change_exec_date(request, pk):
    if request.method == 'PUT':
        request_data = load_request_data(request)
        ticket = models.Ticket.objects.get(pk=pk)
        if ticket.is_active:
            new_exec_date = request_data.get('status')
            ticket.execution_date = new_exec_date
            ticket.save()
            return JsonResponse(
                {
                    'message': ['Дата выезда', 'Дата выезда успешно изменена.'],
                    'status': 'success'
                },
                status=202
            )
        else:
            return is_active_message("Заявка")

@login_required
@permission_required('projecta.change_act_status_field')
def change_act_status(request, pk):
    if request.method == 'PUT':
        request_data = load_request_data(request)
        new_status = request_data.get('status')
        if new_status in [status[0] for status in models.Act.STATUS_CHOICES]:
            act = models.Act.objects.filter(pk=pk)
            if act.is_active:
                act.update(act_status=new_status)
                return JsonResponse(
                    {
                        'message': ['Статус акта', 'Статус успешно изменён.'],
                        'status': 'success'
                    },
                    status=202
                )
            else:
                return is_active_message("Акт")

@login_required
@permission_required('projecta.change_act_status_field')
def change_check_status(request, pk):
    if request.method == 'PUT':
        request_data = load_request_data(request)
        new_status = request_data.get('status')
        if new_status in [status[0] for status in models.Act.CHECK_STATUSES]:
            act = models.Act.objects.filter(pk=pk)
            if act.is_active:
                act.update(check_status=new_status)
                return JsonResponse(
                    {
                        'message': ['Статус счёта', 'Статус успешно изменён.'],
                        'status': 'success'
                    },
                    status=202
                )
            else:
                return is_active_message("Акт")

@login_required
@permission_required('projecta.change_agreement_status_field')
def change_agreement_status(request, pk):
    if request.method == 'PUT':
        request_data = load_request_data(request)
        try:
            agreement = models.Agreement.objects.get(pk=pk)
        except models.Agreement.DoesNotExist:
            return JsonResponse({
                'message': ['Статус договора', 'Данного соглашения не существует'],
                'status': 'danger'
            },
                status=403
            )
        if agreement.client.is_delete:
            return is_delete_message("Клиент")
        elif agreement.is_delete:
            return is_delete_message("Договор")
        else:
            if agreement.client.is_active:
                if agreement.is_active:
                    new_status = request_data.get('status')
                    if new_status in [status[0] for status in models.Agreement.STATUS_CHOICES]:
                        agreement.status = new_status
                        agreement.save()
                        return JsonResponse(
                            {
                                'message': ['Статус договора', 'Статус успешно изменён.'],
                                'status': 'success'
                            },
                            status=202
                        )
                    return JsonResponse(
                        {
                            'message': ['Статус договора', 'Данный статус не доступен'],
                            'status': 'danger'
                        },
                        status=403
                    )
                return is_active_message("Договор")
            return is_active_message("Клиент")

@login_required
@permission_required('projecta.delete_clientcontact')
def delete_contacts(request, pk):
    if request.method == 'DELETE':
        try:
            models.ClientContact.objects.get(pk=pk).delete()
            return JsonResponse(
                {
                    'message': ['Контакт успешно удалён'],
                    'status': 'success'
                },
                status=200
            )
        except IntegrityError:
            return JsonResponse(
                {
                    'message': ['Контакта не существует'],
                    'status': 'warning'
                },
                status=403
            )

@login_required
@permission_required('projecta.delete_insurancepolicy')
def delete_insurance_policy(request, pk):
    if request.method == 'DELETE':
        try:
            models.InsurancePolicy.objects.get(pk=pk).delete()
            return JsonResponse(
                {
                    'message': ['Страховой полис успешно удалён'],
                    'status': 'success'
                },
                status=200
            )
        except IntegrityError:
            return JsonResponse(
                {
                    'message': ['Страховой полис не существует'],
                    'status': 'warning'
                },
                status=403
            )

@login_required
@permission_required('projecta.delete_equipment')
def delete_equipment(request, pk):
    if request.method == 'DELETE':
        try:
            models.Equipment.objects.get(pk=pk).delete()
            return JsonResponse(
                {
                    'message': ['Оборудование успешно удалено'],
                    'status': 'success'
                },
                status=200
            )
        except IntegrityError:
            return JsonResponse(
                {
                    'message': ['Оборудования не существует'],
                    'status': 'warning'
                },
                status=403
            )

@login_required
@permission_required('projecta.can_create_excel_file')
def excel_create_handler(request):
    company = request.user.executor
    pages = request.GET['params'].split(',')
    if len(pages) == 0:
        return HttpResponse(status=403)
    elif 'all' in pages:
        pages = []
    creator = CreatorXLSX(company, pages)
    creator.create_file()
    return FileResponse(open(creator.filename, 'rb'), as_attachment=True)