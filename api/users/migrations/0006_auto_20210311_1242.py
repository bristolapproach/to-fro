# Generated by Django 3.0.7 on 2021-03-11 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210311_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='data_consent_date',
            field=models.DateField(help_text='When did this person give their consent to keeping their data in ToFro?', verbose_name='Data agreement date'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='daily_digest_optin',
            field=models.BooleanField(default=False, verbose_name='Daily digest opt-in'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='weekly_digest_optin',
            field=models.BooleanField(default=False, verbose_name='Weekly digest opt-in'),
        ),
    ]
