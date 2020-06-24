# Generated by Django 3.0.7 on 2020-06-23 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200512_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='external_volunteer_id',
            field=models.CharField(blank=True, help_text='The ID of the volunteer in an external system', max_length=50, null=True),
        ),
    ]