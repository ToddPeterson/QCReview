# Generated by Django 2.2.4 on 2019-08-19 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qc_review', '0002_qcrun_codeline'),
    ]

    operations = [
        migrations.AddField(
            model_name='qcrun',
            name='attempt',
            field=models.IntegerField(default=1),
        ),
    ]
