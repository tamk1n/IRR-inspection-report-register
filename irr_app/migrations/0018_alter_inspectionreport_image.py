# Generated by Django 4.2.4 on 2023-10-19 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irr_app', '0017_alter_inspectionreport_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectionreport',
            name='image',
            field=models.ImageField(null=True, upload_to='evidences'),
        ),
    ]