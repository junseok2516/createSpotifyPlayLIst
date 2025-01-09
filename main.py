# Create a Spotify playlist from Today's billboard top100 charts 
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime as dt


URL="https://www.billboard.com/charts/hot-100/"
response = requests.get(url=URL)
# print(response.text)

soup = BeautifulSoup(response.text, "html.parser")

spotify_ClientID = "YOUR_SPOTIFY_CLIENT_ID"
spotify_ClientSecret = "YOUR_SPOTIFY_CLIENT_SECRET"
redirect_URL = "https://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=spotify_ClientID,
        client_secret=spotify_ClientSecret,
        redirect_uri=redirect_URL,
        scope="playlist-modify-private",
    )
)
user_id = sp.current_user()["id"]

this_year = dt.date.today().year

billboard_song_names = soup.find_all(name="h3", class_="a-no-trucate")
# print(billboard_song_names)
song_names = [song.getText().strip() for song in billboard_song_names]
# print(song_names)
song_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{this_year}")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} dosen't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{this_year} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)