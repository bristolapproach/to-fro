# Generated by Django 3.0.7 on 2021-02-24 16:22

from django.db import migrations
import uuid

def gen_uuid(apps, schema_editor):
    Action = apps.get_model('actions', 'Action')
    for row in Action.objects.all():
        row.action_uuid = uuid.uuid4()
        row.save(update_fields=['action_uuid'])

class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0002_action_action_uuid'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
