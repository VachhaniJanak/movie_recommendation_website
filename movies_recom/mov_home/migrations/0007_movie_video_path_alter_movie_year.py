# Generated by Django 4.2 on 2024-07-24 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mov_home', '0006_alter_movie_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='video_path',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.DateField(default='2024-07-24', null=True),
        ),
    ]
