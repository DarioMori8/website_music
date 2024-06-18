# Generated by Django 5.0.6 on 2024-05-30 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songbird', '0003_playlist_play_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='play_count',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
