from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import SMSMessage
from twilio.rest import Client
from rest_framework import generics
from rest_framework.response import Response
from .serializers import SMSMessageSerializer, SMSMessageListSerializer,DeliveryReportSerializer


class SMSMessageList(generics.ListAPIView):
    serializer_class = SMSMessageListSerializer
    queryset = SMSMessage.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




MESSAGE = "Hello, Your results are ready at the hospital, Kindly indicate when you will pick the result\n1. 1 day\n2. 2 day\n3. 3 days\n4. 4 days"


@api_view(['POST'])
def send_sms(request):
    # Parse and validate the input data using a serializer
    serializer = SMSMessageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Get the validated phone number from the serializer
    phone_number = serializer.validated_data['phone_number']

    # Initialize the Twilio client with your account SID and auth token
    client = Client("", "")

    # Send the SMS message
    message = client.messages.create(
        to=phone_number,
        body=MESSAGE,
        from_=""
    )

    # Save the SMS to the database with the current time as the sent time
    sent_time = datetime.now()
    sms = SMSMessage(
        message=MESSAGE,
        phone_number=phone_number,
        message_id=message.sid,
        date_sent=sent_time,
    )
    sms.save()

    # Return a response with the message status and the sent time
    return Response({
        'success': True,
        'status': message.status,
        'sent_time': sent_time.strftime('%Y-%m-%d %H:%M:%S'),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def handle_delivery_report(request):
    # Get the message ID and status from the request data
    message_id = request.data.get('MessageSid')
    status = request.data.get('MessageStatus')

    # Update the SMS in the database with the delivered time
    if message_id and status == 'delivered':
        sms = SMSMessage.objects.get(message_id=message_id)
        sms.date_delivered = datetime.now()
        sms.save()

    # Return a response with a status of 200 OK
    return Response({'success': True}, status=status.HTTP_200_OK)



@api_view(['POST'])
def handle_incoming_message(request):
    # Get the incoming message details from the request data
    body = request.data.get('Body')
    message_id = request.data.get('MessageSid')
    phone_number = request.data.get('From')

    # Update the SMS in the database with the incoming message details
    sms = SMSMessage.objects.get(message_id=message_id)
    sms.body = body
    sms.date_received = datetime.now()
    
    # Update the SMS in the database with the read time
    sms.date_read = datetime.now()
    sms.save()

    # Add your own custom logic to handle the user's incoming message
    # ...

    # Return a response with a status of 200 OK
    return Response({'success': True}, status=status.HTTP_200_OK)
