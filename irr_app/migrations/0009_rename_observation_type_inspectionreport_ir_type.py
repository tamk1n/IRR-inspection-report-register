# Generated by Django 4.2.4 on 2023-10-03 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('irr_app', '0008_division_company'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inspectionreport',
            old_name='observation_type',
            new_name='ir_type',
        ),
    ]