# Generated by Django 3.0.5 on 2020-05-26 20:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0010_auto_20200521_1537'),
        ('actions', '0010_merge_20200526_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='help_type',
            field=models.ForeignKey(help_text='Which kind of help is needed', null=True, on_delete=django.db.models.deletion.PROTECT, to='categories.HelpType', verbose_name='Action type'),
        ),
        migrations.AlterField(
            model_name='action',
            name='requested_datetime',
            field=models.DateTimeField(help_text='When should the action be completed by?', null=True, verbose_name='Due'),
        ),
    ]
