import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from requests.exceptions import ReadTimeout
from spotipy.exceptions import SpotifyException

# Authentication configuration
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='Your client id',
                                               client_secret='Your client secret',
                                               redirect_uri='http://localhost:8888/callback',
                                               scope='playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'))

# Get user playlists
def get_user_playlists():
    results = sp.current_user_playlists()
    playlists = results['items']
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])
    return playlists

# Function to choose a playlist
def choose_playlist(playlists):
    print("Playlists retrieved.")
    for idx, playlist in enumerate(playlists):
        print(f"{idx + 1}: {playlist['name']}")
    choice = int(input("Choose a playlist: ")) - 1
    if 0 <= choice < len(playlists):
        print(f"You selected: {playlists[choice]['name']}")
        return playlists[choice]['id']
    else:
        print("Invalid selection.")
        return None

# Get tracks from a playlist
def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

# Classify tracks by artist
def classify_tracks_by_artist(tracks):
    artist_dict = {}
    for item in tracks:
        track = item['track']
        artist_id = track['artists'][0]['id']
        artist_name = track['artists'][0]['name']
        if artist_name not in artist_dict:
            artist_dict[artist_name] = []
        artist_dict[artist_name].append(track['id'])
    return artist_dict

# Classify tracks by similar artists
def classify_tracks_by_similar_artists(tracks):
    similar_artist_dict = {}
    for item in tracks:
        track = item['track']
        artist_id = track['artists'][0]['id']
        artist_name = track['artists'][0]['name']
        while True:
            try:
                related_artists = sp.artist_related_artists(artist_id)['artists']
                break
            except ReadTimeout:
                print(f"Timeout while fetching related artists for {artist_name}. Retrying...")
                time.sleep(5)
            except SpotifyException as e:
                if e.http_status == 429:
                    retry_after = int(e.headers.get('Retry-After', 1))
                    print(f"Rate limit reached. Waiting for {retry_after} seconds...")
                    time.sleep(retry_after)
                else:
                    raise e
        for related_artist in related_artists:
            related_artist_name = related_artist['name']
            if related_artist_name not in similar_artist_dict:
                similar_artist_dict[related_artist_name] = []
            similar_artist_dict[related_artist_name].append(track['id'])
        # Small delay to avoid hitting the rate limit
        time.sleep(0.1)
    return similar_artist_dict

# Create new playlists
def create_playlist(user_id, name, track_ids):
    new_playlist = sp.user_playlist_create(user_id, name)
    # Add tracks in batches of 100
    for i in range(0, len(track_ids), 100):
        sp.playlist_add_items(new_playlist['id'], track_ids[i:i+100])
    return new_playlist['id']

# Example usage
user_id = sp.me()['id']
playlists = get_user_playlists()
selected_playlist_id = choose_playlist(playlists)
if selected_playlist_id:
    tracks = get_playlist_tracks(selected_playlist_id)
    
    # Ask user if they want to group by artist or by similar artists
    choice = input("Do you want to group by artist (A) or by similar artists (S)? ").strip().lower()
    
    if choice == 'a':
        classified_tracks = classify_tracks_by_artist(tracks)
        print("Tracks classified by artist.")
    elif choice == 's':
        classified_tracks = classify_tracks_by_similar_artists(tracks)
        print("Tracks classified by similar artists.")
    else:
        print("Invalid option.")
        exit()
    
    for artist, track_ids in classified_tracks.items():
        if track_ids:
            print(f"Creating playlist for artist: {artist}")
            create_playlist(user_id, f"{artist} Playlist", track_ids)
            print(f"Playlist created for artist: {artist}")
        else:
            print(f"No tracks found for artist: {artist}")
else:
    print("No valid playlist selected.")
