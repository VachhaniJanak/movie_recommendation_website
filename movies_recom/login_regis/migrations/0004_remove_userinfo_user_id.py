# Generated by Django 4.2 on 2024-09-21 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_regis', '0003_ratemovie_movie_ratemovie_rate_ratemovie_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='user_id',
        ),
    ]
