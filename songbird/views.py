import json
from typing import Counter
import warnings
from django.shortcuts import render,  redirect, get_object_or_404
from .models import *
from django.contrib.auth import  authenticate, login, logout
from .forms import UserRegistrationForm
from .forms import UserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from .forms import UserProfileForm, PlaylistForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST,require_GET
from django.db.models import Q



    


def songbird(request):
    
    songs = Song.objects.all()
    top_songs = Song.objects.order_by('-play_count')[:15]

    # Ottenere le prime 10 playlist più ascoltate
    top_playlists = Playlist.objects.filter(is_public= True).order_by('-play_count')[:10]
    playlist_groups = [top_playlists[i:i + 5] for i in range(0, len(top_playlists), 5)]

    return render(request, 'songbird/home.html', {'user': request.user,'top_songs': top_songs, 'playlist_groups': playlist_groups, 'songs':songs})


def check_authentication(request):
    if request.user.is_authenticated:
        return JsonResponse({'authenticated': True})
    else:
        return JsonResponse({'authenticated': False})


@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_playlists = Playlist.objects.filter(user=request.user)
    favorite_songs = user_profile.favorite_songs.all()
    context = {
        'user': request.user,
        'user_profile': user_profile,
        'user_playlists': user_playlists,
        'favorite_songs': favorite_songs,
    }
    return render(request, 'songbird/profile.html', context)



def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'songbird/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'songbird/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  


@login_required
@csrf_protect
def increment_playlist_play_count(request, playlist_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        listened_songs_count = data.get('listened_songs_count')
        playlist = get_object_or_404(Playlist, id=playlist_id)
        user = request.user

        if user != playlist.user and playlist.is_public and int(listened_songs_count) >= 3:
            playlist.increment_play_count()
            return JsonResponse({'success': True, 'play_count': playlist.play_count})
    
    return JsonResponse({'success': False})
        


def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    context = {
        'playlist': playlist
    }
    return render(request, 'songbird/playlist_detail.html', context)


@login_required
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    if request.method == 'POST':
        playlist.delete()
        return redirect('user_playlists')
    return render(request, 'songbird/confirm_delete.html', {'playlist': playlist})


@login_required
def favorite_songs(request):
    user_profile = UserProfile.objects.get(user=request.user)
    favorite_songs = user_profile.favorite_songs.all()
    context = {
        'favorite_songs': favorite_songs,
    }
    return render(request, 'songbird/favorite_songs.html', context)

@login_required
def check_favorite(request, song_id):
    user = request.user
    try:
        song = Song.objects.get(id=song_id)
        is_favorite = song in user.userprofile.favorite_songs.all()
        return JsonResponse({'is_favorite': is_favorite})
    except Song.DoesNotExist:
        return JsonResponse({'error': 'Song not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    


@login_required
def user_playlists(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'songbird/user_playlists.html', {'playlists': playlists})


@login_required
def get_user_playlists(request):
    playlists = Playlist.objects.filter(user=request.user).values('id', 'name')
    return JsonResponse({'playlists': list(playlists)})



@login_required
def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            playlist.update_genre()  
            form.save_m2m() 
            return redirect('profile') 
    else:
        form = PlaylistForm()
    return render(request, 'songbird/create_playlist.html', {'form': form})



@login_required
@csrf_exempt
def toggle_favorite(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if song in user_profile.favorite_songs.all():
        user_profile.favorite_songs.remove(song)
        is_favorite = False
    else:
        user_profile.favorite_songs.add(song)
        is_favorite = True

    return JsonResponse({'is_favorite': is_favorite})

@login_required
@csrf_exempt
def add_to_playlist(request, song_id, playlist_id):
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, id=playlist_id)
        song = get_object_or_404(Song, id=song_id)
        if song not in playlist.songs.all():
            playlist.add_song(song)
            playlist.update_genre() 
            return JsonResponse({'message': 'Song added to playlist successfully!'})
        else:
            return JsonResponse({'message': 'Song is already in the playlist.'})
    return JsonResponse({'message': 'Invalid request'}, status=400)

def remove_song_from_playlist(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    song = get_object_or_404(Song, id=song_id)
    if song in playlist.songs.all():
        playlist.remove_song(song)
        playlist.update_genre()  
    return redirect('playlist_detail', playlist_id=playlist.id)

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'songbird/edit_profile.html', {'form': form})




@require_POST
@csrf_exempt  
def toggle_playlist_public(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    if request.user == playlist.user:
        data = json.loads(request.body)
        playlist.is_public = data['is_public']
        playlist.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=403)


def increment_play_count_song(request, song_id):
    if request.method == "POST":
        song = get_object_or_404(Song, id=song_id)
        song.increment_play_count_song()
        return JsonResponse({'success': True, 'play_count': song.play_count})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
    





@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    user_profile = UserProfile.objects.get(user=user_to_follow)
    request.user.userprofile.following.add(user_profile)
    return redirect('follow_profile', user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    user_profile = UserProfile.objects.get(user=user_to_unfollow)
    request.user.userprofile.following.remove(user_profile)
    return redirect('follow_profile', user_id=user_id)

@login_required
def following_list(request):
    user_profile = request.user.userprofile
    following = user_profile.following.all()
    return render(request, 'songbird/following_list.html', {'following': following})

@login_required
def follow_profile(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    playlists = Playlist.objects.filter(user=user_profile.user, is_public=True)
    playlist_groups = [playlists[i:i + 5] for i in range(0, len(playlists), 5)]
    return render(request, 'songbird/follow_profile.html', {
        'user_profile': user_profile,
        'playlists': playlists,
        'playlist_groups': playlist_groups
    })




def search(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', 'all')

    songs = playlists = users = artists = genres = None
    if  request.user.is_authenticated:
        current_user = request.user  

    if filter_type == 'all':
        songs = Song.objects.filter(
            Q(title__icontains=query) |
            Q(artist__icontains=query) |
            Q(genre__icontains=query)
        )
        if  request.user.is_authenticated:
            other_public_playlists = Playlist.objects.exclude(user=current_user).filter(is_public=True)
            user_playlists = Playlist.objects.filter(user=current_user)

            playlists = other_public_playlists | user_playlists
        else:
            other_public_playlists = Playlist.objects.filter(is_public=True)
            playlists = other_public_playlists

        users = User.objects.filter(username__icontains=query)
        artists = Song.objects.filter(artist__icontains=query).values('artist').distinct()
        genres = Song.objects.filter(genre__icontains=query).values('genre').distinct()
    elif filter_type == 'song':
        songs = Song.objects.filter(
            Q(title__icontains=query) |
            Q(artist__icontains=query) |
            Q(genre__icontains=query)
        )
    elif filter_type == 'playlist':
        if  request.user.is_authenticated:

            playlists = Playlist.objects.exclude(user=current_user).filter(
                Q(name__icontains=query) |
                Q(genre__icontains=query),
                is_public=True
            )
            user_playlists = Playlist.objects.filter(
                Q(name__icontains=query) |
                Q(genre__icontains=query),
                user=current_user
            )
            playlists = playlists | user_playlists
        else:
            playlists = Playlist.objects.filter(
                Q(name__icontains=query) |
                Q(genre__icontains=query),
                is_public=True
            )
            playlists = playlists

        
    elif filter_type == 'user':
        users = User.objects.filter(username__icontains=query)
    elif filter_type == 'artist':
        artists = Song.objects.filter(artist__icontains=query).values('artist').distinct()
    elif filter_type == 'genre':
        genres = Song.objects.filter(genre__icontains=query).values('genre').distinct()

    context = {
        'query': query,
        'filter_type': filter_type,
        'songs': songs,
        'playlists': playlists,
        'users': users,
        'artists': artists,
        'genres': genres,
    }
    return render(request, 'songbird/search.html', context)


def artist_songs(request, artist_name):
    songs = Song.objects.filter(artist=artist_name)

    context = {
        'artist_name': artist_name,
        'songs': songs,
    }
    return render(request, 'songbird/artist_songs.html', context)

@login_required
def recommendations(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=request.user)
    favorite_songs = user_profile.favorite_songs.all()

    favorite_genres = favorite_songs.values_list('genre', flat=True)
    genre_counts = Counter(favorite_genres)
    top_genres = [genre for genre, _ in genre_counts.most_common(3)]

    # Ottenere 10 canzoni suggerite basate sui generi preferiti
    recommended_songs = Song.objects.filter(genre__in=top_genres).exclude(id__in=favorite_songs).distinct()[:10]

    public_playlists = Playlist.objects.filter(is_public=True).exclude(user=user)
    
    # Filtrare le playlist che corrispondono ai generi preferiti
    matching_playlists = []
    for playlist in public_playlists:
        playlist_genres = [genre.strip() for genre in playlist.genre.split('&')]
        if any(genre in top_genres for genre in playlist_genres):
            matching_playlists.append(playlist)

    # Prendere solo le prime 3 playlist
    matching_playlists = matching_playlists[:3]

    context = {
        'recommended_songs': recommended_songs,
        'recommended_playlists': matching_playlists
    }

    return render(request, 'songbird/recommendations.html', context)


def genre_detail(request, genre_name):
    songs = Song.objects.filter(genre=genre_name)
    public_playlists = Playlist.objects.filter(is_public=True)

    if not request.user.is_authenticated:
        all_playlists = public_playlists
    else:
        current_user = request.user
        private_playlists = Playlist.objects.filter(is_public=False, user=current_user)
        all_playlists= public_playlists | private_playlists

    # Filtrare le playlist che corrispondono ai generi preferiti
    matching_playlists = []
    for playlist in all_playlists:
        playlist_genres = [genre.strip() for genre in playlist.genre.split('&')]
        if any(genre in genre_name for genre in playlist_genres):
            matching_playlists.append(playlist)


    context = {
        'genre': genre_name,
        'songs': songs,
        'playlists': matching_playlists
    }
    return render(request, 'songbird/genre_detail.html', context)