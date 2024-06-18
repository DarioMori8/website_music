# Generated by Django 5.0.6 on 2024-06-06 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songbird', '0012_alter_playlist_play_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='following', to='songbird.userprofile'),
        ),
    ]