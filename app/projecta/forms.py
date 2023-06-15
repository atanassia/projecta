from django import forms

from . import models


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = [
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "phone",
            "position",
        ]

class ExecutorForm(forms.ModelForm):
    class Meta:
        model = models.Executor
        fields = [
            "inn",
            "kpp",
            "org_form",
            "name",
            "legal_address",
            "index",
            "phone",
            "email",
        ]

class ClientForm(forms.ModelForm):
    email = forms.EmailField(max_length=255, label="Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.non_required:
            self.fields[field].required = False

    class Meta:
        model = models.Client
        fields = [
            "inn",
            "kpp",
            "name",
            "org_form",
            "legal_address",
            "status",
            "index",
            "phone",
            "email",
        ]
        non_required = ["kpp", "status", "org_form", "legal_address", "index", "email"]

class ClientContactForm(forms.ModelForm):
    class Meta:
        model = models.ClientContact
        fields = ["fio", "phone", "email", "priority"]

class ClientStatusForm(forms.ModelForm):
    class Meta:
        model = models.ClientStatus
        fields = ["client", "status"]

class AgreementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        company = kwargs.pop("company")
        super().__init__(*args, **kwargs)
        self.fields["responsible"] = forms.ChoiceField(
            choices=[
                (worker.id, worker)
                for worker in company.workers.filter(
                    position="Plumber",
                    is_superuser=False,
                )
            ],
            label="Ответственный",
        )

        self.fields["client"] = forms.ChoiceField(
            choices=[(client.id, client) for client in company.clients.filter(is_active=True, is_delete=False)],
            label="Клиент",
        )
        license_choices = [("Нет лицензии", "Нет лицензии")]
        license_choices.extend(
            [(license.license, license.license) for license in company.licenses.all()]
        )
        self.fields["license"] = forms.ChoiceField(
            choices=license_choices, label="Лицензия"
        )
        self.fields["status"].empty_label = None
        self.fields["reasons_termination"].empty_label = None
        self.fields["client"].empty_label = None
        self.fields["num_reg_certificate"].required = False
        self.fields["date_reg_certificate"].required = False

    class Meta:
        model = models.Agreement
        fields = [
            "agreement_number",
            "num_reg_certificate",
            "date_reg_certificate",
            "status",
            "reasons_termination",
            "client",
            "address",
            "responsible",
            "date_from",
            "date_to",
            "class_danger",
            "license",
        ]

class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Executor
        fields = ["inn", "kpp", "name", "legal_address", "index", "phone", "email"]

class AgreementUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        company = kwargs.pop("company")
        agreement = kwargs.pop("agreement")
        super().__init__(*args, **kwargs)
        self.fields["responsible"] = forms.ChoiceField(
            choices=[
                (worker.id, worker)
                for worker in company.workers.filter(
                    position="Plumber",
                    is_superuser=False,
                )
            ],
            label="Ответственный",
        )
        license_choices = [("Нет лицензии", "Нет лицензии")]
        license_choices.extend(
            [(license.license, license.license) for license in company.licenses.all()]
        )
        self.fields["license"] = forms.ChoiceField(
            choices=license_choices, label="Лицензия", initial=agreement.license
        )
        self.fields["status"].empty_label = None
        self.fields["reasons_termination"].empty_label = None
        self.fields["date_reg_certificate"].required = False
        self.fields["num_reg_certificate"].required = False

        self.fields["client"] = forms.ChoiceField(
            choices=[(client.pk, client) for client in company.clients.filter(is_active=True, is_delete=False)],
            label="Клиент",
        )

        self.fields["is_active"] = forms.BooleanField(initial=agreement.is_active, required=False, label="Активен?")

    class Meta:
        model = models.Agreement
        fields = [
            "client",
            "agreement_number",
            "num_reg_certificate",
            "date_reg_certificate",
            "status",
            "reasons_termination",
            "address",
            "responsible",
            "date_from",
            "date_to",
            "class_danger",
            "license",
            "is_active"
        ]

class AgreementStatusForm(forms.ModelForm):
    class Meta:
        model = models.AgreementStatus
        fields = ["agreement", "status"]

class EquipmentForm(forms.ModelForm):
    def __init__(self, *args, company, **kwargs):
        super(EquipmentForm, self).__init__(*args, **kwargs)
        self.fields["agreement"] = forms.ChoiceField(
            choices=[(item.pk, item) for item in company.agreements.filter(is_active=True, is_delete=False)],
            label="Соглашения",
        )

        self.fields["agreement"].empty_label = None
        self.fields["type"].empty_label = None

    class Meta:
        model = models.Equipment
        fields = ["agreement", "type", "description", "amount", "date_from", "date_to"]

class InsurancePolicyForm(forms.ModelForm):
    def __init__(self, *args, company, **kwargs):
        super(InsurancePolicyForm, self).__init__(*args, **kwargs)
        self.fields["agreement"] = forms.ChoiceField(
            choices=[(item.pk, item) for item in company.agreements.filter(is_active=True, is_delete=False)],
            label="Соглашения",
        )

        self.fields["agreement"].empty_label = None
        self.fields["date_from"].empty_label = None

    class Meta:
        model = models.InsurancePolicy
        fields = [
            "agreement",
            "name_insurance_company", 
            "date_from",
            "date_to"
        ]

class TicketForm(forms.ModelForm):
    def __init__(self, *args, company, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields["status"].empty_label = None
        self.fields["type"].empty_label = None
        self.fields["agreement"] = forms.ChoiceField(
            choices=[(item.pk, item) for item in company.agreements.filter(is_active=True, is_delete=False)],
            label="Соглашения",
        )
        self.fields["agreement"].empty_label = None

    class Meta:
        model = models.Ticket
        fields = ["type", "status", "agreement", "comment", "execution_date"]

class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = models.TicketStatus
        fields = ["ticket", "status"]

class ActForm(forms.ModelForm):
    def __init__(self, *args, company, **kwargs):
        super(ActForm, self).__init__(*args, **kwargs)

        self.fields["act_status"].empty_label = None
        self.fields["agreement"] = forms.ChoiceField(
            choices=[(item.pk, item) for item in company.agreements.filter(is_active=True, is_delete=False)],
            label="Соглашения",
        )
        self.fields["agreement"].empty_label = None
        self.fields["check_status"].empty_label = None
        self.fields["check_number"].required = False
        self.fields["check_status"].required = False

    class Meta:
        model = models.Act
        fields = [
            "act_number",
            "agreement",
            "act_date",
            "act_status",
            "check_number",
            "check_status",
        ]

class EquipmentPhotoForm(forms.ModelForm):
    class Meta:
        model = models.EquipmentPhoto
        fields = ["photo"]
        widgets = {
            "photo": forms.ClearableFileInput(attrs={"multiple": True}),
        }
