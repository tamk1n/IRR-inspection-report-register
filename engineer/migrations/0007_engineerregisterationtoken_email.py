# Generated by Django 4.2.4 on 2023-11-03 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engineer', '0006_alter_engineerregisterationtoken_expired_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='engineerregisterationtoken',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='User email'),
        ),
    ]