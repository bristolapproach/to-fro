# Generated by Django 3.0.7 on 2020-11-22 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coordinator_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('complete', 'Complete')], default='pending', max_length=30),
        ),
    ]
