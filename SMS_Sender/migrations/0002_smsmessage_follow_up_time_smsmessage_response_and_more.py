# Generated by Django 4.1.7 on 2023-04-01 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS_Sender', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='smsmessage',
            name='follow_up_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='smsmessage',
            name='response',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='smsmessage',
            name='message',
            field=models.TextField(),
        ),
    ]
