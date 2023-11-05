# Generated by Django 4.2.4 on 2023-11-05 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irr_app', '0019_inspectionreport_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectionreport',
            name='status',
            field=models.CharField(blank=True, choices=[('Open', 'Open'), ('Close', 'Close'), ('Overdue', 'Overdue')], default='Open', null=True),
        ),
    ]
