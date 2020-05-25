from django.db import migrations
from categories.models import Requirement, HelpType
import json


def import_helptype_requirements(apps, schema_editor):
    enhanced_dbs_requirement = Requirement.objects.get_or_create(
        name='Enhanced DBS Check')
    enhanced_dbs_requirement[0].help_types.set(HelpType.objects.all())
    enhanced_dbs_requirement[0].save()


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0008_helptype_requirements'),
    ]

    operations = [
        migrations.RunPython(import_helptype_requirements),
    ]
