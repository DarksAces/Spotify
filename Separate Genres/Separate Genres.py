import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from requests.exceptions import ReadTimeout
from spotipy.exceptions import SpotifyException

# Configuración de autenticación
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='Your Client ID',
                                               client_secret='Your Secret Client',
                                               redirect_uri='http://localhost:8888/callback',
                                               scope='playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private'))

# Obtener listas de reproducción del usuario
def get_user_playlists():
    results = sp.current_user_playlists()
    playlists = results['items']
    while results['next']:
        results = sp.next(results)
        playlists.extend(results['items'])
    return playlists

# Función para elegir la playlist
def elegir_playlist(playlists):
    print("Listas de reproducción obtenidas.")
    for idx, playlist in enumerate(playlists):
        print(f"{idx + 1}: {playlist['name']}")
    choice = int(input("Elige una playlist: ")) - 1
    if 0 <= choice < len(playlists):
        print(f"Has elegido: {playlists[choice]['name']}")
        return playlists[choice]['id']
    else:
        print("Selección inválida.")
        return None

# Obtener pistas de una lista de reproducción
def get_playlist_tracks(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

# Clasificar pistas por género
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
                print(f"Timeout al obtener géneros para el artista {artist_name}. Reintentando...")
                time.sleep(5)
            except SpotifyException as e:
                if e.http_status == 429:
                    retry_after = int(e.headers.get('Retry-After', 1))
                    print(f"Alcanzado el límite de tasa. Esperando {retry_after} segundos...")
                    time.sleep(retry_after)
                else:
                    raise e
        print(f"Géneros para el artista {artist_name}: {genres}")
        for genre in genres:
            genre_lower = genre.lower()
            if genre_lower in genre_dict:
                genre_dict[genre_lower].append(track_id)
        # Añadiendo un pequeño retraso para evitar la tasa límite
        time.sleep(0.1)
    return genre_dict

# Crear nuevas listas de reproducción
def create_playlist(user_id, name, track_ids):
    new_playlist = sp.user_playlist_create(user_id, name)
    # Añadir pistas en lotes de 100
    for i in range(0, len(track_ids), 100):
        sp.playlist_add_items(new_playlist['id'], track_ids[i:i+100])
    return new_playlist['id']

# Ejemplo de uso
user_id = sp.me()['id']
playlists = get_user_playlists()
selected_playlist_id = elegir_playlist(playlists)
if selected_playlist_id:
    tracks = get_playlist_tracks(selected_playlist_id)
    
    # Solicitar géneros al usuario
    genres_to_classify = input("Introduce los géneros a clasificar separados por comas: ").split(',')
    genres_to_classify = [genre.strip().lower() for genre in genres_to_classify]
    
    classified_tracks = classify_tracks_by_genre(tracks, genres_to_classify)
    print("Pistas clasificadas por género.")
    
    for genre, track_ids in classified_tracks.items():
        if track_ids:
            print(f"Creando playlist para el género: {genre}")
            create_playlist(user_id, f"{genre} Playlist", track_ids)
            print(f"Playlist creada para el género: {genre}")
        else:
            print(f"No se encontraron pistas para el género: {genre}")
else:
    print("No se seleccionó ninguna playlist válida.")
