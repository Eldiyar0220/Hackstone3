# Generated by Django 3.1 on 2021-07-02 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='like',
        ),
    ]