from django.db import migrations
import json
from actions.models import Action, ActionStatus


def import_requirements(apps, schema_editor):
    """
    Update existing action statuses for tasks to account for "ONGOING"
    being inserted between "COMPLETED" and "COULDNT_COMPLETE"
    """
    Action.objects.filter(action_status=ActionStatus.COMPLETED) \
        .update(action_status=ActionStatus.COULDNT_COMPLETE)
    Action.objects.filter(action_status=ActionStatus.ONGOING) \
        .update(action_status=ActionStatus.COMPLETED)


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0006_auto_20200521_1537'),
    ]

    operations = [
        migrations.RunPython(import_requirements),
    ]
