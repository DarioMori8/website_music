# Generated by Django 5.0.6 on 2024-06-03 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songbird', '0010_remove_song_favorited_by_userprofile_favorite_songs'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
