# Generated by Django 4.2 on 2024-08-02 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mov_home', '0008_alter_movie_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.DateField(default='2024-08-02', null=True),
        ),
    ]
