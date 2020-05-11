from django.db import migrations
import json


def import_helptype_icon_names(apps, schema_editor):
    # We can't import the models directly as they may be a newer
    # version than this migration expects. We use the historical versions.
    HelpType = apps.get_model('categories', 'HelpType')

    # Load the data.
    with open("categories/initial_data/help_types.json") as data_file:
        data = json.load(data_file)

    # Create the objects.
    for help_type in data:
        HelpType.objects.filter(name=help_type.get('name')).update(
            icon_name=help_type.get('icon_name'))


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_helptype_icon_name'),
    ]

    operations = [
        migrations.RunPython(import_helptype_icon_names),
    ]
