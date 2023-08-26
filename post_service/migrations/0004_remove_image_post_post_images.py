# Generated by Django 4.2.4 on 2023-08-26 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_service', '0003_rename_id_post_image_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='images',
            field=models.ManyToManyField(related_name='id_post', to='post_service.image'),
        ),
    ]
