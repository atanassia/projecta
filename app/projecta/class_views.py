from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
# from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

from projecta import models, forms

# delete in clients and agreements

# DETAIL VIEWS
# ----------------------------------------------------------------------
class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'projecta.view_client'
    template_name = 'projecta/client_detail.html'
    model = models.Client
    context_object_name = 'client'

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('projecta:main'))

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context['agreement_form'] = forms.AgreementForm(company=self.request.user.executor)

        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.object.is_delete:
            return redirect('projecta:clients')
        return super().render_to_response(context, **response_kwargs)


class AgreementDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'projecta.view_agreement'
    template_name = 'projecta/agreement_detail.html'
    model = models.Agreement
    context_object_name = 'agreement'

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('projecta:main'))

    def get_context_data(self, **kwargs):
        context = super(AgreementDetailView, self).get_context_data(**kwargs)
        company = self.request.user.executor

        context['ticket_form'] = forms.TicketForm(company=company)
        context['policy_form'] = forms.InsurancePolicyForm(company=company)
        context['act_form'] = forms.ActForm(company=company)
        context['equipment_form'] = forms.EquipmentForm(company=company)
        context['ticket_statuses'] = models.Ticket.STATUS_CHOICES
        context['ticket_types'] = models.Ticket.TYPE_CHOICES
        context['agreement_statuses'] = models.Agreement.STATUS_CHOICES

        return context

    def render_to_response(self, context, **response_kwargs):
        if self.object.is_delete:
            return redirect('projecta:agreements')
        return super().render_to_response(context, **response_kwargs)


class TicketDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'projecta.view_ticket'
    template_name = 'projecta/ticket_detail.html'
    model = models.Ticket
    context_object_name = 'ticket'

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('projecta:main'))

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        context['act'] = context['ticket'].agreement.acts.filter(
            act_date__year=context['ticket'].created.year,
            act_date__month=context['ticket'].created.month
        ).first()
        context['ticket_types'] = models.Ticket.TYPE_CHOICES
        context['ticket_statuses'] = models.Ticket.STATUS_CHOICES
        context['agreement_statuses'] = models.Agreement.STATUS_CHOICES
        context['act_statuses'] = models.Act.STATUS_CHOICES
        context['check_statuses'] = models.Act.CHECK_STATUSES

        return context


# UPDATE VIEWS
# ----------------------------------------------------------------------
class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'projecta.change_client'
    template_name = 'projecta/client_update.html'
    model = models.Client
    context_object_name = 'client'
    fields = ['inn', 'kpp', 'name', 'org_form', 'legal_address', 'status', 'index', 'phone', 'email', 'is_active']

    def get_form(self, form_class=None):
        form = super(ClientUpdateView, self).get_form(form_class)
        form.fields['org_form'].required = False
        form.fields['kpp'].required = False
        form.fields['status'].required = False
        form.fields['legal_address'].required = False
        form.fields['index'].required = False
        form.fields['email'].required = False
        return form

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('projecta:main'))
    
    def render_to_response(self, context, **response_kwargs):
        if self.object.is_delete:
            return redirect('projecta:clients')
        return super().render_to_response(context, **response_kwargs)


class LicenseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'projecta.change_license'
    template_name = 'projecta/update_license.html'
    model = models.License
    context_object_name = 'license'
    fields = ['license', 'date_reg', 'class_danger']

    def form_valid(self, form):
        data = self.request.POST
        curr_license = data['curr_license'].strip()
        new_license = data['license'].strip()
        company = self.request.user.executor
        company.agreements.filter(license=curr_license).update(
            license=new_license,
            class_danger=data['class_danger'][0]
        )
        return super(LicenseUpdateView, self).form_valid(form)


class InsurancePolicyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'projecta.change_insurancepolicy'
    template_name = 'projecta/insurance_policy_update.html'
    model = models.InsurancePolicy
    context_object_name = 'insurance_policy'
    fields = ['name_insurance_company', 'date_from', 'date_to']

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('projecta:main'))

class EquipmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'projecta.change_equipment'
    template_name = 'projecta/equipment_update.html'
    model = models.Equipment
    context_object_name = 'equipment'
    fields = ['type', 'description', 'amount', 'date_from', 'date_to']

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('projecta:main'))


class ContactUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'projecta.change_clientcontact'
    template_name = 'projecta/contact_update.html'
    model = models.ClientContact
    context_object_name = 'contact'
    fields = ['fio', 'phone', 'email', 'priority']

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('projecta:main'))


class ActUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'projecta.change_act'
    template_name = 'projecta/act_update.html'
    model = models.Act
    context_object_name = 'act'
    fields = ['act_number', 'act_date', 'act_status',
              'check_number', 'check_status']

    def get_form(self, form_class=None):
        form = super(ActUpdateView, self).get_form(form_class)
        form.fields['check_number'].required = False
        form.fields['check_status'].required = False
        return form

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('projecta:main'))

    def form_valid(self, form):
        context = super(ActUpdateView, self).get_context_data()
        act = context['act']
        queryset = act.agreement.acts.filter(
            act_date__startswith=datetime.strptime(
                str(act.act_date),
                '%Y-%m-%d'
            ).strftime('%Y-%m')
        )
        if not queryset.exists() or act in queryset:
            return super(ActUpdateView, self).form_valid(form)
        else:
            context['error'] = {
                'message': 'Акт за эту дату уже существует',
                'status': 'danger'
            }
            return render(self.request, 'projecta/act_update.html', context=context)


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'projecta.change_user'
    template_name = 'projecta/user_update.html'
    model = models.User
    context_object_name = 'worker'
    fields = ['email', 'first_name', 'last_name', 'middle_name', 'phone', 'position', 'is_active']

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('projecta:main'))

    def form_valid(self, form):
        user = form.save()
        user.groups.clear()
        user.groups.add(Group.objects.get(name=user.position))

        return super(UserUpdateView, self).form_valid(form)
