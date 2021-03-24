# Generated by Django 3.0.7 on 2021-03-23 23:20

from django.db import migrations
from actions.utils import copy_volunteers, copy_feedback

def forwards(apps, schema_editor):
    copy_volunteers()
    copy_feedback()


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0007_auto_20210323_2308'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop)
    ]
