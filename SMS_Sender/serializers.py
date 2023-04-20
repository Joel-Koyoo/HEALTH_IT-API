from rest_framework import serializers
from .models import SMSMessage
from datetime import datetime
from twilio.rest import Client

from rest_framework import serializers
from .models import SMSMessage


class SMSMessageListSerializer(serializers.ModelSerializer):
    sent_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    delivered_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    read_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = SMSMessage
        fields = ('sent_time', 'phone_number', 'message', 'message_id', 'date_sent', 'delivered_time', 'date_delivered', 'read_time', 'date_read', 'response', 'follow_up_time')


class SMSMessageSerializer(serializers.Serializer):
    message = serializers.CharField(required=False)
    phone_number = serializers.CharField()

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        message = validated_data.get('message', MESSAGE)

        # Save the SMS to the database with the current time as the sent time
        sent_time = datetime.now()
        sms = SMSMessage(
            message=message,
            phone_number=phone_number,
            date_sent=sent_time,
        )
        sms.save()

        # Initialize the Twilio client with your account SID and auth token
        client = Client("", "")

        # Send the SMS message
        message = client.messages.create(
            to=phone_number,
            body=message,
            from_="+15854604566"
        )

        # Update the SMS in the database with the message ID and status
        sms.message_id = message.sid
        sms.status = message.status
        sms.save()

        return sms



class DeliveryReportSerializer(serializers.Serializer):
    MessageSid = serializers.CharField()
    MessageStatus = serializers.CharField()

    def update(self, instance, validated_data):
        message_id = validated_data.get('MessageSid')
        status = validated_data.get('MessageStatus')

        # Update the SMS in the database with the delivered time
        if message_id and status == 'delivered':
            instance.date_delivered = datetime.now()
            instance.save()

        # Update the SMS in the database with the read time
        if message_id and status == 'read':
            instance.date_read = datetime.now()
            instance.save()

        return instance
