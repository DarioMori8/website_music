# Django Music Streaming Site

Welcome to our Django-based music streaming site! This README provides an overview of the site's features and functionalities.

## Table of Contents
- [Features](#features)
- [Home Page](#home-page)
- [Playlist Details](#playlist-details)
- [Song Controls](#song-controls)
- [Favorite Songs](#favorite-songs)
- [Adding Songs to Playlists](#adding-songs-to-playlists)
- [Suggestions](#suggestions)
- [Navigation Bar](#navigation-bar)
- [Search Page](#search-page)
- [User Profile](#user-profile)
- [Creating Playlists](#creating-playlists)
- [Installation and Setup](#installation-and-setup)

## Features
- Home page with a playlist carousel.
- Detailed view of playlists and their songs.
- Controls to play, restart, and stop songs.
- Add or remove songs from favorites.
- Add songs to specific user playlists.
- Song and playlist suggestions.
- Full search functionality.
- User profile management.
- Creation and management of user playlists.

## Home Page
The home page includes:
- A playlist carousel. Clicking on a playlist opens its details.
- A list of songs with play and stop controls. Double-clicking on play restarts the song.
- A heart icon to add/remove songs from favorites.
- A "+" icon to add songs to your playlists.
- A button at the bottom that opens a page with song and playlist suggestions.
The playlists displayed are only public ones, and only the most listened-to songs and playlists by various users are selected.

## Playlist Details
Clicking on a playlist in the carousel opens a detailed view showing all the songs in the playlist.

## Song Controls
- **Play**: Click once to play, double-click to restart.
- **Stop**: Click to stop the song.
- **Favorites**: Click on the heart icon to add a song to favorites. Click again to remove it.

## Adding Songs to Playlists
- Click on the "+" icon next to a song.
- Select the playlist you want to add the song to.

## Suggestions
- At the bottom of the home page, the button opens a suggestions page.
- Suggestions include songs and playlists you might like.
- The functionality within the page is similar to the home page.

## Navigation Bar
- **Logo**: Clicking the logo takes you back to the home page.
- **Profile Icon**: 
  - If you are not logged in, it redirects to the login/registration page.
  - If you are logged in, it opens your profile page.
- **Search Icon**: Opens the search page.

## Search Page
- Search among users, songs, playlists, artists, or genres.
- Clicking on search results opens the corresponding pages:
  - **User**: Opens the user profile with the follow/unfollow button and their public playlists.
  - **Artist**: Opens a page with the artist's songs.
  - **Genre**: Opens a page with songs and playlists of that genre.
  - **Playlist**: Opens the detailed view of the playlist.
- Filters can be activated by clicking the buttons below the search bar.

## User Profile
- **Edit Button (bottom right)**: Allows you to edit bio, username, profile picture, etc.
- **Left Buttons**:
  - **Favorites**: List of your favorite songs.
  - **Following**: List of users you follow.
  - **Playlists**: List of your playlists. Click to view details or add new playlists.

## Creating Playlists
- Navigate to your profile and click the button in your playlist list to create a new playlist.
- Enter the playlist name.
- Optionally, add songs and check the last box to set the playlist as public. If checked, the playlist will be public.
- Save the new playlist.

## Installation and Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
