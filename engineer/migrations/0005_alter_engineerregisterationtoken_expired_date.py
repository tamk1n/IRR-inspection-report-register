# Generated by Django 4.2.4 on 2023-10-29 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engineer', '0004_alter_engineerregisterationtoken_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engineerregisterationtoken',
            name='expired_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
