# Generated by Django 4.2.4 on 2023-08-26 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post_service', '0002_rename_id_user_post_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='id_post',
            new_name='post',
        ),
    ]