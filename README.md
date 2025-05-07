
🎧 General Project Description (English)
============================================================

This repository contains two Python applications designed to help organize and classify Spotify playlists using the Spotify Web API via the Spotipy library. Both apps require user authentication and interaction with Spotify data to reorganize tracks automatically into new playlists.

- Project 1: Classifies playlist tracks by artist or by similar artists.
- Project 2: Classifies playlist tracks by genre, based on artist metadata.

These tools are useful for music lovers who want to automate playlist curation based on musical attributes.


🎧 Descripción General del Proyecto (Español)
============================================================

Este repositorio contiene dos aplicaciones en Python diseñadas para ayudar a organizar y clasificar listas de reproducción de Spotify usando la API Web de Spotify a través de la biblioteca Spotipy. Ambas aplicaciones requieren autenticación del usuario e interactúan con datos de Spotify para reorganizar automáticamente las canciones en nuevas playlists.

- Proyecto 1: Clasifica las pistas de una playlist por artista o por artistas similares.
- Proyecto 2: Clasifica las pistas de una playlist por género, basado en los metadatos del artista.

Estas herramientas son útiles para los amantes de la música que desean automatizar la creación de playlists según atributos musicales.


🔑 How to Get Your Spotify Client ID and Secret (English)
============================================================

1. **Create a Spotify Developer Account:**
   - Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Log in with your Spotify account, or create a new one if you don’t have one.

2. **Create an App:**
   - Once logged in, click on **"Create an App"**.
   - Fill out the necessary fields:
     - **App Name:** Choose a name for your app (this can be anything).
     - **App Description:** Add a brief description of your app (e.g., "Playlist Organizer").
     - **Redirect URI:** This is needed for authentication. You can use `http://localhost:8888/callback` or any URL that fits your app (make sure it matches what you use in your code).
   
3. **Get Client ID and Client Secret:**
   - After creating your app, you'll be redirected to the app's dashboard.
   - Here, you'll find your **Client ID** and **Client Secret**. These are the values you’ll need to input in your code.


🔑 Cómo Obtener Tu Client ID y Client Secret de Spotify (Español)
============================================================

1. **Crear una Cuenta de Desarrollador de Spotify:**
   - Visita el [Panel de Desarrolladores de Spotify](https://developer.spotify.com/dashboard/applications).
   - Inicia sesión con tu cuenta de Spotify, o crea una nueva si no tienes una.

2. **Crear una Aplicación:**
   - Una vez que hayas iniciado sesión, haz clic en **"Crear una Aplicación"**.
   - Completa los campos necesarios:
     - **Nombre de la Aplicación:** Elige un nombre para tu aplicación (esto puede ser lo que desees).
     - **Descripción de la Aplicación:** Agrega una breve descripción de tu aplicación (por ejemplo, "Organizador de Playlists").
     - **Redirect URI:** Esto es necesario para la autenticación. Puedes usar `http://localhost:8888/callback` o cualquier URL que se ajuste a tu aplicación (asegúrate de que coincida con la que usas en tu código).

3. **Obtener el Client ID y Client Secret:**
   - Después de crear tu aplicación, serás redirigido al panel de la aplicación.
   - Aquí encontrarás tu **Client ID** y **Client Secret**. Estos son los valores que necesitarás ingresar en tu código.
