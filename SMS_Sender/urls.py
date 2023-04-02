from django.urls import path
from .views import send_sms, handle_delivery_report, handle_incoming_message, SMSMessageList

urlpatterns = [
    path('send_sms/', send_sms, name='send_sms'),
    path('handle_delivery_report/', handle_delivery_report, name='handle_delivery_report'),
    path('sms_list/', SMSMessageList.as_view(), name='sms_list'),
    path('handle_incoming_message/', handle_incoming_message, name='handle_incoming_message'),
]
