# Generated by Django 3.0.5 on 2020-05-12 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0004_seed_helptype_icon_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]