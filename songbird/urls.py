from django.conf.urls.static import static
from django.urls import path
from . import views
from django.conf import  settings


urlpatterns=[
    path('', views.songbird, name= 'home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name="register"), 
    path('profile/', views.profile, name ='profile' ),
    path('song/', views.song_list, name ='song'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('search/', views.search, name='search'),
    path('artist/<str:artist_name>/', views.artist_songs, name='artist_songs'),
    path('genre/<str:genre_name>/', views.genre_detail, name='genre_detail'),
    path('check_authentication/', views.check_authentication, name='check_authentication'),






    path('follow_profile/<int:user_id>/', views.follow_profile, name='follow_profile'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('following/', views.following_list, name='following_list'),


    path('increment_play_count_song/<int:song_id>/', views.increment_play_count_song, name='increment_play_count_song'),
    path('favorite_songs/', views.favorite_songs, name='favorite_songs'),
    path('toggle_favorite/<int:song_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('check_favorite/<int:song_id>/', views.check_favorite, name='check_favorite'),
    path('recommendations/', views.recommendations, name='recommendations'),



    path('playlists/', views.user_playlists, name='user_playlists'),
    path('get_user_playlists/', views.get_user_playlists, name='get_user_playlists'),

    path('create_playlist/', views.create_playlist, name='create_playlist'),
    path('toggle_playlist_public/<int:playlist_id>/', views.toggle_playlist_public, name='toggle_playlist_public'),
    path('add_to_playlist/<int:song_id>/<int:playlist_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('playlist/<int:playlist_id>/remove_song/<int:song_id>/', views.remove_song_from_playlist, name='remove_song_from_playlist'),
    path('playlists/<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),
    path('increment_playlist_play_count/<int:playlist_id>/', views.increment_playlist_play_count, name='increment_playlist_play_count'),


    path('edit_profile/', views.edit_profile, name='edit_profile'),


  

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)