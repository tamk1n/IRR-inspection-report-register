# Generated by Django 4.2.4 on 2023-10-07 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irr_app', '0009_rename_observation_type_inspectionreport_ir_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspectionreport',
            name='company',
        ),
        migrations.AlterField(
            model_name='inspectionreport',
            name='project',
            field=models.CharField(blank=True, help_text='Project Name', max_length=1000, null=True, verbose_name='Project Name'),
        ),
    ]