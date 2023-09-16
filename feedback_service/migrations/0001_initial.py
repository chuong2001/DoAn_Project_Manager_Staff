# Generated by Django 4.2.4 on 2023-09-14 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_service', '0004_rename_usernamee_account_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id_feedback', models.AutoField(primary_key=True, serialize=False)),
                ('time_feedback', models.DateTimeField()),
                ('content', models.TextField()),
                ('is_read', models.IntegerField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_service.user')),
            ],
        ),
    ]
