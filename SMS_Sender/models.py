from django.db import models

class SMSMessage(models.Model):
    message = models.TextField()
    phone_number = models.CharField(max_length=20)
    message_id = models.CharField(max_length=50, null=True, blank=True)
    date_sent = models.DateTimeField()
    date_delivered = models.DateTimeField(null=True, blank=True)
    date_read = models.DateTimeField(null=True, blank=True)
    response = models.CharField(max_length=10, null=True, blank=True)
    follow_up_time = models.DateTimeField(null=True, blank=True)


    def __str__(self) -> str:
        return self.phone_number
