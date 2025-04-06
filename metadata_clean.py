
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

# ✅ Your real Spotify Developer credentials
CLIENT_ID = 'f191c08bc7c8474bb153c147004897b1'
CLIENT_SECRET = '6aa04c79794140e1a1248ae0b4964068'

# ✅ Set up Spotipy with Client Credentials flow
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

# 🔍 Extract the item type and Spotify ID from a track or album URL
def extract_id(url):
    pattern = r'spotify\.com/(track|album)/([a-zA-Z0-9]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1), match.group(2)
    return None, None

# 🎧 Print metadata for a single track
def print_track(track):
    print(f"\n🎵 Track: {track['name']}")
    print(f"🎤 Artist(s): {', '.join([artist['name'] for artist in track['artists']])}")
    print(f"💿 Album: {track['album']['name']}")
    print(f"📅 Release Date: {track['album']['release_date']}")
    print(f"🏷️ Label: {track['album'].get('label', 'Not available')}")
    print(f"🔖 ISRC: {track['external_ids'].get('isrc', 'Not available')}")

# 📀 Print metadata for an album and all its tracks (with ISRCs)
def print_album(album):
    print(f"\n💿 Album: {album['name']}")
    print(f"🎤 Artist(s): {', '.join([artist['name'] for artist in album['artists']])}")
    print(f"📅 Release Date: {album['release_date']}")
    print(f"🏷️ Label: {album.get('label', 'Not available')}")
    print(f"🔢 Total Tracks: {album['total_tracks']}")

    print("\n🔎 Track List with ISRCs:")
    for track in album['tracks']['items']:
        try:
            track_data = sp.track(track['id'])  # Fetch full track metadata
            isrc = track_data['external_ids'].get('isrc', 'Not available')
            print(f"- 🎵 {track['name']} | ISRC: {isrc}")
        except Exception as e:
            print(f"- 🎵 {track['name']} | ⚠️ Error retrieving ISRC: {e}")

# 🚀 Main logic
def main():
    url = input("Paste a Spotify track or album URL: ")
    item_type, item_id = extract_id(url)

    if item_type == "track":
        print_track(sp.track(item_id))
    elif item_type == "album":
        print_album(sp.album(item_id))
    else:
        print("❌ Invalid or unsupported URL")

if __name__ == "__main__":
    main()
