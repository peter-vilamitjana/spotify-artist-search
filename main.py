import queue
import webbrowser

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from artist import SpotifyArtist
from spotify_api import search_artist, spotify


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buscador de Artistas - Spotify")
        self.setGeometry(100, 100, 600, 800)
        self.is_dark_mode = False
        self.update_style()

        # Crear una lista para almacenar el historial de búsquedas
        self.search_history = []  # Usaremos una lista en lugar de una cola

        # Widgets
        self.artistEntry = QLineEdit(self)
        self.artistEntry.setPlaceholderText("Buscar Artista")
        self.artistEntry.setFont(QFont("Arial", 14))
        self.artistEntry.setStyleSheet(self.get_entry_style())

        self.searchButton = QPushButton("Buscar", self)
        self.searchButton.setFont(QFont("Arial", 14))
        self.searchButton.setStyleSheet(self.get_button_style())
        self.searchButton.clicked.connect(self.queue_search_artist)

        self.previousSearchButton = QPushButton("Búsqueda Anterior", self)
        self.previousSearchButton.setFont(
            QFont("Arial", 14),
        )  # Tamaño de fuente más pequeño
        self.previousSearchButton.setStyleSheet(self.get_button_style())
        self.previousSearchButton.clicked.connect(self.show_previous_search)

        self.toggleButton = QPushButton("Modo Oscuro", self)
        self.toggleButton.setFont(QFont("Arial", 14))
        self.toggleButton.setStyleSheet(self.get_button_style())
        self.toggleButton.clicked.connect(self.toggle_dark_mode)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(10, 150, 580, 400)
        self.scrollArea.setWidgetResizable(True)

        self.resultWidget = QWidget()
        self.scrollArea.setWidget(self.resultWidget)
        self.resultLayout = QVBoxLayout(self.resultWidget)

        layout = QVBoxLayout()
        layout.addWidget(self.artistEntry)
        layout.addWidget(self.searchButton)
        layout.addWidget(
            self.previousSearchButton
        )  # Añadir el botón de búsqueda anterior
        layout.addWidget(self.toggleButton)
        layout.addWidget(self.scrollArea)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_entry_style(self):
        return (
            """
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
        """
            if not self.is_dark_mode
            else """
            border: 1px solid #555;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
            background-color: #333;
            color: white;
        """
        )

    def get_button_style(self):
        return (
            """
            background-color: #1DB954;
            color: white;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
        """
            if not self.is_dark_mode
            else """
            background-color: #444;
            color: white;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
        """
        )

    def update_style(self):
        self.setStyleSheet(
            "background-color: white;"
            if not self.is_dark_mode
            else "background-color: #222;"
        )

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.update_style()
        self.artistEntry.setStyleSheet(self.get_entry_style())
        self.searchButton.setStyleSheet(self.get_button_style())
        self.toggleButton.setStyleSheet(self.get_button_style())
        self.previousSearchButton.setStyleSheet(self.get_button_style())

    def queue_search_artist(self):
        """Realiza la búsqueda del artista y lo añade al historial."""
        artist_name = self.artistEntry.text()
        self.search_artist(artist_name)

    def search_artist(self, artist_name):
        """Realiza la búsqueda del artista y guarda el resultado en el historial."""
        artist_data = search_artist(artist_name)
        if artist_data:
            artist = SpotifyArtist(artist_data, spotify)

            # Guardamos la búsqueda actual en el historial
            self.search_history.append(artist)

            self.display_artist(artist)
        else:
            self.clear_results()
            self.resultLayout.addWidget(QLabel("Artista no encontrado.", self))

    def show_previous_search(self):
        """Muestra la búsqueda anterior almacenada en el historial."""
        if len(self.search_history) > 1:
            # Mostrar el penúltimo artista del historial
            previous_artist = self.search_history[-2]
            self.display_artist(previous_artist)
        else:
            self.clear_results()
            self.resultLayout.addWidget(QLabel("No hay búsqueda anterior.", self))

    def display_artist(self, artist):
        """Muestra la información del artista en la interfaz."""
        self.clear_results()  # Limpiar antes de mostrar el artista nuevo o anterior

        if artist.get_image_url():
            image_data = requests.get(artist.get_image_url()).content
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            img_label = QLabel(self)
            img_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            self.resultLayout.addWidget(img_label)

        artist_name_label = QLabel(artist.get_name(), self)
        artist_name_label.setFont(QFont("Arial", 20, QFont.Bold))
        artist_name_label.setStyleSheet(
            "color: black;" if not self.is_dark_mode else "color: white;"
        )
        self.resultLayout.addWidget(artist_name_label)

        followers_label = QLabel(f"Seguidores: {artist.get_followers():,}", self)
        followers_label.setFont(QFont("Arial", 20))
        followers_label.setStyleSheet(
            "color: gray;" if not self.is_dark_mode else "color: lightgray;"
        )
        self.resultLayout.addWidget(followers_label)

        url_label = QLabel(f"Perfil: {artist.get_spotify_url()}", self)
        url_label.setFont(QFont("Arial", 14))
        url_label.setStyleSheet("color: #1DB954;")
        self.resultLayout.addWidget(url_label)

        tracks_label = QLabel("Canciones más reconocidas:", self)
        tracks_label.setFont(QFont("Arial", 16, QFont.Bold))
        tracks_label.setStyleSheet(
            "color: black;" if not self.is_dark_mode else "color: white;"
        )
        self.resultLayout.addWidget(tracks_label)

        for track in artist.get_top_tracks()[:5]:
            track_label = QLabel(track["name"], self)
            track_label.setFont(QFont("Arial", 14))
            track_label.setStyleSheet(
                "color: black;" if not self.is_dark_mode else "color: white;"
            )
            self.resultLayout.addWidget(track_label)
            track_label.mousePressEvent = lambda event, url=track["external_urls"][
                "spotify"
            ]: self.open_in_spotify(url)

    def clear_results(self):
        """Limpia todos los resultados actuales en la interfaz."""
        for i in reversed(range(self.resultLayout.count())):
            widget_to_remove = self.resultLayout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.deleteLater()

    def open_in_spotify(self, track_url):
        """Abre la canción en Spotify usando el navegador."""
        webbrowser.open(track_url)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
