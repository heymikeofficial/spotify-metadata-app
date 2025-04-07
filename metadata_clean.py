import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import timedelta
import re

# Spotify credentials
CLIENT_ID = 'f191c08bc7c8474bb153c147004897b1'
CLIENT_SECRET = '6aa04c79794140e1a1248ae0b4964068'

# Spotify API setup
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

# Extract type and ID from Spotify URL
def extract_id(url):
    pattern = r'spotify\.com/(track)/([a-zA-Z0-9]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1), match.group(2)
    return None, None

# Format duration (ms to mm:ss)
def format_duration(ms):
    seconds = int(ms / 1000)
    return str(timedelta(seconds=seconds))[2:]

# Streamlit app setup
st.set_page_config(page_title="Spotify Metadata Checker", layout="centered")
st.title("🎧 Spotify Metadata Checker")
st.caption("Paste a Spotify track URL to view its metadata.")

# ✅ THIS is the input box that must show up
url = st.text_input("Spotify Track URL", placeholder="https://open.spotify.com/track/xyz123")

if url:
    item_type, item_id = extract_id(url)

    if item_type == "track":
        try:
            track = sp.track(item_id)
            album = sp.album(track['album']['id'])

            # Gather all artist names
            artist_names = [artist['name'] for artist in track['artists']]
            artist_ids = [artist['id'] for artist in track['artists']]

            # Pull genres from all listed artists
            all_genres = []
            for artist_id in artist_ids:
                artist_info = sp.artist(artist_id)
                artist_genres = artist_info.get('genres', [])
                all_genres.extend(artist_genres)

            genre_set = set(all_genres)
            genre_display = ", ".join(sorted(genre_set)) if genre_set else "Not listed on Spotify"

            st.image(album['images'][0]['url'], width=300)
            st.subheader(track['name'])

            st.markdown(f"**Primary Artist(s):** {', '.join(artist_names)}")
            st.markdown(f"**Genre(s):** {genre_display}")
            st.markdown(f"**Release Date:** {album['release_date']}")
            st.markdown(f"**ISRC:** {track['external_ids'].get('isrc', 'Not available')}")
            st.markdown(f"**Label:** {album.get('label', 'Not available')}")
            st.markdown(f"**Explicit:** {'Yes' if track['explicit'] else 'No'}")
            st.markdown(f"**Duration:** {format_duration(track['duration_ms'])}")

            st.markdown("---")
            st.markdown("🔗 **Spotify Link:**")
            st.link_button("Open in Spotify", track['external_urls']['spotify'])

        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter a valid Spotify **track** URL.")
