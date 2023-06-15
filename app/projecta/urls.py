from django.urls import path
from . import views
from . import handlers
from . import class_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'projecta'

urlpatterns = [
    path('main/', views.main_view, name='main'),
    path('clients/', views.client_view, name='clients'),
    path('workers/', views.worker_view, name='workers'),
    path('agreement/', views.agreement_view, name='agreements'),
    path('insurance_policies/', views.insurance_policy_view, name='insurance_policies'),
    path('tickets/', views.ticket_view, name='tickets'),
    path('acts/', views.act_view, name='acts'),
    path('company/', views.executor_detail_view, name='company'),
    path('equipment/', views.equipment_view, name='equipment'),
    # detail views
    path('client/<int:pk>', class_views.ClientDetailView.as_view(),
         name='client_detail'),
    path('agreement/<int:pk>', class_views.AgreementDetailView.as_view(),
         name='agreement_detail'),

    path('ticket/<int:pk>', class_views.TicketDetailView.as_view(),
         name='ticket_detail'),

    # update views
    path('client/update/<int:pk>', class_views.ClientUpdateView.as_view(),
         name='client_update'),
    path('agreement/update/<int:pk>', views.agreement_update_view,
         name='agreement_update'),
    path('company/update/', views.executor_update_view,
         name='company_update'),
    path('equipment/update/<int:pk>', class_views.EquipmentUpdateView.as_view(),
         name='equipment_update'),
    path('contacts/update/<int:pk>', class_views.ContactUpdateView.as_view(),
         name='contact_update'),
    path('insurance_policy/update/<int:pk>', class_views.InsurancePolicyUpdateView.as_view(),
         name='insurance_policy_update'),
    path('act/update/<int:pk>', class_views.ActUpdateView.as_view(),
         name='act_update'),
    path('user/update/<int:pk>', class_views.UserUpdateView.as_view(),
         name='user_update'),

    # creating and changing handlers
    path('license/update/<int:pk>', class_views.LicenseUpdateView.as_view(), name='update_license'),

    path('create/agreement', handlers.create_agreement, name='create_agreement'),
    path('create/client', handlers.create_client, name='create_client'),
    path('create/act', handlers.create_act, name='create_act'),
    path('create/ticket', handlers.create_ticket, name='create_ticket'),
    path('create/contact', handlers.create_contacts, name='create_contact'),
    path('create/equipment', handlers.create_equipment, name='create_equipment'),
    path('create/user', handlers.create_user, name='create_user'),
    path('create/license', handlers.create_license, name='create_license'),
    path('create/insurance_policies', handlers.create_insurance_policy, name='create_insurance_policy'),

    path('add-photo/<int:pk>', views.add_equipment_photo_view,
         name='add_photo'),

     # PUT status update handlers
     path('update/client_delete/<int:pk>', handlers.change_client_is_delete,
          name='update_client_is_delete'),
     path('update/agreement_delete/<int:pk>', handlers.change_agreement_is_delete,
          name='update_agreement_is_delete'),
     path('update/ticket_status/<int:pk>', handlers.change_ticket_status,
         name='update_ticket_status'),
     path('update/ticket-execution-date/<int:pk>', handlers.change_exec_date,
         name='update_ticket_exec_date'),
     path('update/ticket_type/<int:pk>', handlers.change_ticket_type,
         name='update_ticket_type'),
     path('update/agreement_status/<int:pk>', handlers.change_agreement_status,
         name='update_agreement_status'),
     path('update/act_status/<int:pk>', handlers.change_act_status,
         name='update_act_status'),
     path('update/check_status/<int:pk>', handlers.change_check_status,
         name='update_check_status'),
     path('update/ticket_comment/<int:pk>', handlers.change_ticket_comment,
         name='update_ticket_comment'),

    # delete views
    path('delete/contact/<int:pk>', handlers.delete_contacts, name='delete_contact'),
    path('delete/insurance_policy/<int:pk>', handlers.delete_insurance_policy, name='delete_insurance_policy'),
    path('delete/equipment/<int:pk>', handlers.delete_equipment, name='delete_equipment'),
    path('delete/equipment-photo/<int:pk>', handlers.delete_equipment_photo,
         name='delete_equip_photo'),
    # authenticate views
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change_password/', views.password_change_view, name='change_password'),


    path('excel-create/', handlers.excel_create_handler, name='create_excel')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
