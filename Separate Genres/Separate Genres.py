import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from requests.exceptions import ReadTimeout
from spotipy.exceptions import SpotifyException

# Authentication configuration
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='Your Client ID',
                                               client_secret='Your Secret Client',
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
        print(f"You have chosen: {playlists[choice]['name']}")
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

# Classify tracks by genre
def classify_tracks_by_genre(tracks, genres_to_classify):
    genre_dict = {genre: [] for genre in genres_to_classify}
    for item in tracks:
        track = item['track']
        track_id = track['id']
        artist_id = track['artists'][0]['id']
        artist_name = track['artists'][0]['name']
        while True:
            try:
                genres = sp.artist(artist_id)['genres']
                break
            except ReadTimeout:
                print(f"Timeout while fetching genres for artist {artist_name}. Retrying...")
                time.sleep(5)
            except SpotifyException as e:
                if e.http_status == 429:
                    retry_after = int(e.headers.get('Retry-After', 1))
                    print(f"Rate limit reached. Waiting for {retry_after} seconds...")
                    time.sleep(retry_after)
                else:
                    raise e
        print(f"Genres for artist {artist_name}: {genres}")
        for genre in genres:
            genre_lower = genre.lower()
            if genre_lower in genre_dict:
                genre_dict[genre_lower].append(track_id)
        # Adding a small delay to avoid rate limit issues
        time.sleep(0.1)
    return genre_dict

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
    
    # Request genres from the user
    genres_to_classify = input("Enter the genres to classify, separated by commas: ").split(',')
    genres_to_classify = [genre.strip().lower() for genre in genres_to_classify]
    
    classified_tracks = classify_tracks_by_genre(tracks, genres_to_classify)
    print("Tracks classified by genre.")
    
    for genre, track_ids in classified_tracks.items():
        if track_ids:
            print(f"Creating playlist for the genre: {genre}")
            create_playlist(user_id, f"{genre} Playlist", track_ids)
            print(f"Playlist created for the genre: {genre}")
        else:
            print(f"No tracks found for the genre: {genre}")
else:
    print("No valid playlist selected.")
