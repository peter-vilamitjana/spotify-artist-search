from abc import ABC, abstractmethod


class Artist(ABC):
    """Clase abstracta que representa a un artista."""

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_followers(self):
        pass

    @abstractmethod
    def get_image_url(self):
        pass

    @abstractmethod
    def get_spotify_url(self):
        pass

    @abstractmethod
    def get_top_tracks(self):
        pass


class SpotifyArtist(Artist):
    """Implementación de la clase abstracta para artistas en Spotify."""

    def __init__(self, artist_data, spotify_instance):
        self.artist_data = artist_data
        self.spotify = spotify_instance

    def get_name(self):
        return self.artist_data["name"]

    def get_followers(self):
        return self.artist_data["followers"]["total"]

    def get_image_url(self):
        return (
            self.artist_data["images"][0]["url"] if self.artist_data["images"] else None
        )

    def get_spotify_url(self):
        return self.artist_data["external_urls"]["spotify"]

    def get_top_tracks(self):
        return self.spotify.artist_top_tracks(self.artist_data["id"])["tracks"]
