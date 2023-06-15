from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import *

admin.site.index_title = "Администрирование сайта || Газовое оборудование"
admin.site.site_header = "Панель администратора || Газовое оборудование "
admin.site.site_title = ""

admin.site.register(Act)
admin.site.register(ActStatus)

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"

@admin.register(Executor)
class ExecutorAdmin(admin.ModelAdmin):
    list_display = ("id", "inn", "kpp", "upper_full_name", "legal_address", "index", "phone", "email", "lower_created", "lower_updated")
    list_filter = ("org_form", "created", "updated", )
    search_fields = ("id__startswith", "inn__startswith", "index__startswith", "phone__startswith", "email__startswith", "name__startswith", )
    ordering = ['-updated']

    @admin.display(description='Наименование')
    def upper_full_name(self, obj):
        return ('%s "%s"' % (obj.org_form, obj.name)).upper()

    @admin.display(description='Создан')
    def lower_created(self, obj):
        return ("%s" % (obj.created.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

    @admin.display(description='Обновлен')
    def lower_updated(self, obj):
        return ("%s" % (obj.updated.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "upper_full_name", "position", "is_superuser", "is_staff", "is_active", "phone", "email", "executor_id", "lower_created", "lower_updated")
    list_filter = ("position", "is_superuser", "is_staff", "is_active", "created", "updated", )
    ordering = ['-updated']

    @admin.display(description='Name')
    def upper_full_name(self, obj):
        return ("%s %s %s" % (obj.last_name, obj.first_name, obj.middle_name)).upper()

    @admin.display(description='Создан')
    def lower_created(self, obj):
        return ("%s" % (obj.created.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

    @admin.display(description='Обновлен')
    def lower_updated(self, obj):
        return ("%s" % (obj.updated.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "inn", "kpp", "upper_full_name", "legal_address", "index", "phone", "email", "status", "is_active", "is_delete", "executor_id", "author_id", "lower_created", "lower_updated")
    list_filter = ("org_form", "status", "is_active", "is_delete", "created", "updated", )
    search_fields = ("id__startswith", "inn__startswith", "index__startswith", "phone__startswith", "email__startswith", "name__startswith", )
    ordering = ['-updated']

    @admin.display(description='Наименование')
    def upper_full_name(self, obj):
        return ('%s "%s"' % (obj.org_form, obj.name)).upper()

    @admin.display(description='Создан')
    def lower_created(self, obj):
        return ("%s" % (obj.created.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

    @admin.display(description='Обновлен')
    def lower_updated(self, obj):
        return ("%s" % (obj.updated.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

@admin.register(ClientStatus)
class ClientStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "client_id", "status", "is_active", "is_delete", "is_actual", "executor", "author", "lower_created", "lower_updated")
    list_filter = ("is_active", "is_delete", "is_actual", "status", "created", "updated", )
    search_fields = ("client_id__startswith", )
    ordering = ['-updated']

    @admin.display(description='Создан')
    def lower_created(self, obj):
        return ("%s" % (obj.created.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

    @admin.display(description='Обновлен')
    def lower_updated(self, obj):
        return ("%s" % (obj.updated.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

@admin.register(ClientContact)
class ClientContactAdmin(admin.ModelAdmin):
    list_display = ("id", "fio", "phone", "email", "priority", "client_id", "lower_created", "lower_updated")
    list_filter = ("created", "updated", )
    ordering = ['-updated']

    @admin.display(description='Создан')
    def lower_created(self, obj):
        return ("%s" % (obj.created.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

    @admin.display(description='Обновлен')
    def lower_updated(self, obj):
        return ("%s" % (obj.updated.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = ("id", "agreement_number", "address", "lower_date_from", "lower_date_to", "status", "is_active", "is_delete", "reg_certificate", "license", "class_danger", "client_id", "responsible_id", "executor_id", "author_id", "lower_created", "lower_updated")
    list_filter = ("is_active", "is_delete", "status", "date_from", "date_to", "created", "updated", "class_danger", )
    search_fields = ("id__startswith", "agreement_number__startswith", "address__startswith",  "num_reg_certificate__startswith", "license__startswith",)
    ordering = ['-updated']

    @admin.display(description='Сертификат')
    def reg_certificate(self, obj):
        if obj.date_reg_certificate.strftime("%d.%m.%Y") == "01.01.1970":
            date_reg = "Нет сертификата"
        else:
            date_reg = ("(%s г.)" % obj.date_reg_certificate.strftime("%d.%m.%Y"))
        return ("%s %s" % (obj.num_reg_certificate, date_reg))

    @admin.display(description='Дата начала')
    def lower_date_from(self, obj):
        return ("%s г." % (obj.date_from.strftime("%d.%m.%Y"))).lower()

    @admin.display(description='Дата конца')
    def lower_date_to(self, obj):
        return ("%s г." % (obj.date_to.strftime("%d.%m.%Y"))).lower()

    @admin.display(description='Создан')
    def lower_created(self, obj):
        return ("%s" % (obj.created.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

    @admin.display(description='Обновлен')
    def lower_updated(self, obj):
        return ("%s" % (obj.updated.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

@admin.register(AgreementStatus)
class AgreementStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "agreement_id", "status", "responsible", "is_active", "is_delete", "is_actual", "executor", "author", "lower_created", "lower_updated")
    list_filter = ("is_active", "is_delete", "is_actual", "status", "created", "updated", )
    search_fields = ("agreement_id__startswith", )
    ordering = ['-updated']

    @admin.display(description='Создан')
    def lower_created(self, obj):
        return ("%s" % (obj.created.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

    @admin.display(description='Обновлен')
    def lower_updated(self, obj):
        return ("%s" % (obj.updated.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ("id", "name_insurance_company", "lower_date_from", "lower_date_to", "agreement_id", "executor_id", "lower_created", "lower_updated")
    list_filter = ("date_from", "date_to", )
    ordering = ['-updated']

    @admin.display(description='Дата начала')
    def lower_date_from(self, obj):
        return ("%s г." % (obj.date_from.strftime("%d.%m.%Y"))).lower()

    @admin.display(description='Дата конца')
    def lower_date_to(self, obj):
        return ("%s г." % (obj.date_to.strftime("%d.%m.%Y"))).lower()

    @admin.display(description='Создан')
    def lower_created(self, obj):
        return ("%s" % (obj.created.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

    @admin.display(description='Обновлен')
    def lower_updated(self, obj):
        return ("%s" % (obj.updated.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "description", "amount", "lower_period_exploitation", "agreement_id", "executor_id", "lower_created", "lower_updated")
    list_filter = ("type", "date_from", "date_to", )
    ordering = ['-updated']

    @admin.display(description='Период эксплуатации')
    def lower_period_exploitation(self, obj):
        return ("%s г. - %s г." % (obj.date_from.strftime("%d.%m.%Y"), obj.date_to.strftime("%d.%m.%Y"))).lower()

    @admin.display(description='Создан')
    def lower_created(self, obj):
        return ("%s" % (obj.created.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

    @admin.display(description='Обновлен')
    def lower_updated(self, obj):
        return ("%s" % (obj.updated.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "lower_execution_date", "comment", "status", "agreement_id", "author_id", "executor_id", "is_active", "lower_created", "lower_updated")
    list_filter = ("type", "execution_date", "status", "is_active", )
    ordering = ['-updated']

    @admin.display(description='Дата выполнения')
    def lower_execution_date(self, obj):
        return ("%s г." % (obj.execution_date.strftime("%d.%m.%Y"))).lower()

    @admin.display(description='Создан')
    def lower_created(self, obj):
        return ("%s" % (obj.created.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

    @admin.display(description='Обновлен')
    def lower_updated(self, obj):
        return ("%s" % (obj.updated.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

@admin.register(TicketStatus)
class TicketStatusAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "ticket_id", "author", "executor", "is_active", "is_actual", "lower_created", "lower_updated")
    list_filter = ("status", "is_active", "is_actual", )
    ordering = ['-updated']

    @admin.display(description='Создан')
    def lower_created(self, obj):
        return ("%s" % (obj.created.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

    @admin.display(description='Обновлен')
    def lower_updated(self, obj):
        return ("%s" % (obj.updated.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

@admin.register(EquipmentPhoto)
class EquipmentPhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket_id", "executor_id", "get_html_photo", "lower_created")
    fields = ("id", "ticket", "executor", "get_html_photo", "photo", "author_full_name", "lower_created")
    readonly_fields = ("id", "get_html_photo", "author_full_name", "lower_created")
    ordering = ['-created']

    @admin.display(description='Создан')
    def lower_created(self, obj):
        return ("%s" % (obj.created.strftime("%d.%m.%Y, %H:%M:%S"))).lower()

    @admin.display(description='Автор')
    def author_full_name(self, obj):
        return ("%s, %s %s %s (ID= %s)" % (obj.author.position, obj.author.last_name, obj.author.first_name, obj.author.middle_name, obj.author.id))

    @admin.display(description='Фото оборудования')
    def get_html_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width=100>")