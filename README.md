# Spotify Artist Search Application

Este proyecto es una aplicación GUI construida con PyQt5 que permite a los usuarios buscar artistas utilizando la API de
Spotify.

## Tecnologías utilizadas

-   Python
-   PyQt5
-   Spotify API

## Características

-   Búsqueda de artistas
-   Interfaz de usuario con modo oscuro/claro
-   Historial de búsquedas

## Cómo ejecutar

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tuusuario/Spotify_Artist_Search.git
    ```
2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3. Ejecuta el archivo principal:
    ```bash
    python main.py
    ```

## Configuración de las credenciales de Spotify

Para que el programa funcione, necesitas crear un archivo `.env` en la raíz del proyecto con tus credenciales de
Spotify. Para obtener tus credenciales:

1. Crea una cuenta de desarrollador de Spotify en
   [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
2. Crea una nueva aplicación y obtendrás un **Client ID** y un **Client Secret**.
3. Crea un archivo `.env` en la raíz del proyecto y agrega lo siguiente:

```plaintext
SPOTIFY_CLIENT_ID=tu_cliente_id
SPOTIFY_CLIENT_SECRET=tu_cliente_secreto
```
