# Generated by Django 4.2.4 on 2023-10-19 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irr_app', '0014_inspectionreport_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspectionreport',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]