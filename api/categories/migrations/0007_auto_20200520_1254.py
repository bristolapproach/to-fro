# Generated by Django 3.0.5 on 2020-05-20 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0006_seed_requirement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helptype',
            name='icon_name',
            field=models.CharField(blank=True, help_text="Name of the fontawesome icon used to represent this type of help (among the 'free' ones: https://fontawesome.com/icons?d=gallery&m=free)", max_length=50, null=True),
        ),
    ]
