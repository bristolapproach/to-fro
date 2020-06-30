from django.db import migrations
import json


def import_help_types(apps, schema_editor):
    # We can't import the models directly as they may be a newer
    # version than this migration expects. We use the historical versions.
    HelpType = apps.get_model('categories', 'HelpType')

    # Load the data.
    with open("categories/initial_data/help_types.json") as data_file:
        data = json.load(data_file)

    # Create the objects.
    for help_type in data:
        HelpType.objects.create(
            name=help_type.get('name'),
            icon_name=help_type.get('icon_name')
        ).save()


def import_wards(apps, schema_editor):
    Ward = apps.get_model('categories', 'Ward')
    with open("categories/initial_data/wards.json") as data_file:
        data = json.load(data_file)
    for ward in data:
        Ward.objects.create(name=ward).save()


def import_requirements(apps, schema_editor):
    Requirement = apps.get_model('categories', 'Requirement')
    with open("categories/initial_data/requirements.json") as data_file:
        data = json.load(data_file)
    for requirement in data:
        Requirement.objects.create(name=requirement).save()


def import_helptype_requirements(apps, schema_editor):
    Requirement = apps.get_model('categories', 'Requirement')
    HelpType = apps.get_model('categories', 'HelpType')
    enhanced_dbs_requirement = Requirement.objects.get_or_create(
        name='Enhanced DBS Check')
    enhanced_dbs_requirement[0].help_types.set(HelpType.objects.all())
    enhanced_dbs_requirement[0].save()


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_help_types),
        migrations.RunPython(import_wards),
        migrations.RunPython(import_requirements),
        migrations.RunPython(import_helptype_requirements)
    ]
