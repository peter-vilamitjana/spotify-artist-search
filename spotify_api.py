import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
# Configuración de las credenciales de Spotify

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
spotify = spotipy.Spotify(auth_manager=auth_manager)


def search_artist(artist_name):
    result = spotify.search(q=f"artist:{artist_name}", type="artist")
    if result["artists"]["items"]:
        return result["artists"]["items"][0]
    return
