# Generated by Django 5.0.6 on 2024-05-31 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songbird', '0004_alter_playlist_play_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='play_count',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
