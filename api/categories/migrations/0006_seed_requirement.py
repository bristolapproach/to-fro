from django.db import migrations
import json


def import_requirements(apps, schema_editor):
    Requirement = apps.get_model('categories', 'Requirement')
    with open("categories/initial_data/requirements.json") as data_file:
        data = json.load(data_file)
    for requirement in data:
        Requirement.objects.create(name=requirement).save()


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0005_requirement'),
    ]

    operations = [
        migrations.RunPython(import_requirements),
    ]
