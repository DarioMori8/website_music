from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os


# Funzione per generare il percorso personalizzato per le immagini del profilo utente
def user_profile_image_path(instance, filename):
    return os.path.join('img_user', filename)

def song_image_path(instance, filename):
    return os.path.join('img_song', filename)

# Funzione per generare il percorso personalizzato per i file mp3 delle canzoni
def song_file_path(instance, filename):
    return os.path.join('song', filename)

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    length = models.DurationField()
    release_date = models.DateField()
    audio_file = models.FileField(upload_to=song_file_path)
    play_count = models.PositiveIntegerField(default=0, editable=True)

    def __str__(self):
        return self.title

    def get_audio_url(self):
        return self.audio_file.url

    def increment_play_count_song(self):
        self.play_count += 1
        self.save()





class Playlist(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)
    created_at = models.DateTimeField(auto_now_add=True)
    shared_link = models.URLField(blank=True, null=True)
    play_count = models.PositiveIntegerField(default=0, editable=True)
    is_public = models.BooleanField(default=False)
    genre = models.CharField(max_length=255, blank=True, null=True)  

    def __str__(self):
        return f"{self.name} ({'Public' if self.is_public else 'Private'})"

    def increment_play_count(self):
        self.play_count += 1
        self.save()

    def add_song(self, song):
        self.songs.add(song)
        self.update_genre() 

    def remove_song(self, song):
        self.songs.remove(song)
        self.update_genre()  

    def update_genre(self):
        from collections import Counter

        genres = self.songs.values_list('genre', flat=True)

        genre_counts = Counter(genres)

        most_common_genres = genre_counts.most_common(2)

        self.genre = " & ".join([genre for genre, count in most_common_genres])
        self.save()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_image_path, blank=True, null=True)
    favorite_songs = models.ManyToManyField(Song, related_name='favorited_by', blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)


    def __str__(self):
        return self.user.username




