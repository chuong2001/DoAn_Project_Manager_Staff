# Generated by Django 4.2.4 on 2023-08-26 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post_service', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='userr',
        ),
    ]
