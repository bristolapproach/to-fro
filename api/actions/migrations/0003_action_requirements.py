# Generated by Django 3.0.5 on 2020-05-12 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0005_requirement'),
        ('actions', '0002_auto_20200511_0901'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='requirements',
            field=models.ManyToManyField(related_name='actions', to='categories.Requirement',
                                         help_text='Only volunteers matching these requirements will see the action.'),
        ),
    ]