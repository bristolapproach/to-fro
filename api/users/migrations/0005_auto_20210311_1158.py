# Generated by Django 3.0.7 on 2021-03-11 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210311_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='data_consent_date',
            field=models.DateField(help_text='When did this person give their consent to keeping their data in ToFro?'),
        ),
    ]
