import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import requests

API_KEY = "144d5567c992b6007b601538a94fc364"
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

artist_data = []
track_data = []


class Song:
    def __init__(self, title, url, description="", rating=None):
        self.title = title
        self.url = url
        self.description = description
        self.rating = rating


class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def remove_song(self, song_title):
        self.songs = [song for song in self.songs if song.title.lower() != song_title.lower()]

    def list_songs(self):
        return "\n".join([f"{idx+1}. Title: {song.title}\nDescription: {song.description}\nRating: {song.rating or 'N/A'}\n"
                          for idx, song in enumerate(self.songs)])



def save_playlists_to_file(playlists):
    try:
        with open("playlists.txt", "w") as file:
            for playlist in playlists:
                file.write(f"Playlist: {playlist.name}\n")
                for song in playlist.songs:
                    file.write(f"{song.title}\n{song.url}\n{song.description}\n{song.rating or 'N/A'}\n")
                file.write("\n")
    except IOError as e:
        messagebox.showerror("Error", f"An error occurred while saving the playlists: {e}")


def load_playlists_from_file():
    playlists = []
    try:
        with open("playlists.txt", "r") as file:
            lines = file.readlines()
            current_playlist = None
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith("Playlist:"):
                    if current_playlist:
                        playlists.append(current_playlist)
                    playlist_name = line[len("Playlist: "):]
                    current_playlist = Playlist(playlist_name)
                elif line:
                    title = line
                    url = lines[i + 1].strip()
                    description = lines[i + 2].strip()
                    rating_str = lines[i + 3].strip()
                    rating = int(rating_str) if rating_str.isdigit() else None
                    current_playlist.add_song(Song(title, url, description, rating))
                    i += 3
                i += 1
            if current_playlist:
                playlists.append(current_playlist)
    except FileNotFoundError:
        messagebox.showinfo("Info", "No playlists file found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading playlists: {e}")
    return playlists


def get_top_artists():
    params = {
        'method': 'chart.getTopArtists',
        'api_key': API_KEY,
        'format': 'json',
        'limit': 50
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('artists', {}).get('artist', [])
    else:
        messagebox.showerror("API Error", f"Error calling API: {response.status_code}")
        return []


def get_top_tracks(artist_name):
    params = {
        'method': 'artist.getTopTracks',
        'artist': artist_name,
        'api_key': API_KEY,
        'format': 'json',
        'limit': 10
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('toptracks', {}).get('track', [])
    else:
        messagebox.showerror("API Error", f"Error calling API: {response.status_code}")
        return []


def show_top_artists():
    artists = get_top_artists()
    if artists:
        artists_list.delete(0, tk.END)
        global artist_data
        artist_data = artists
        for idx, artist in enumerate(artists, start=1):
            artist_name = artist['name']
            artists_list.insert(tk.END, f"{idx}. {artist_name}")
    else:
        messagebox.showinfo("Info", "No artists found.")

def show_top_tracks(event):
    global track_data
    selection = artists_list.curselection()
    if not selection:
        return
    artist_index = selection[0]
    artist_name = artist_data[artist_index]['name']

    tracks = get_top_tracks(artist_name)
    if tracks:
        tracks_list.delete(0, tk.END)
        track_data = tracks
        for idx, track in enumerate(tracks, start=1):
            track_name = track['name']
            playcount = track.get('playcount', 'N/A')
            tracks_list.insert(tk.END, f"{idx}. {track_name} (Playcount: {playcount})")
    else:
        messagebox.showinfo("Info", f"No tracks found for artist {artist_name}.")


def add_track_to_playlist():
    selection = tracks_list.curselection()
    if not selection:
        messagebox.showwarning("Warning", "No track selected.")
        return

    track_index = selection[0]
    track = track_data[track_index]
    track_name = track['name']
    track_url = track.get('url', "")
    description = f"Artist: {track['artist']['name']}"

    rating = simpledialog.askinteger("Rating", f"Rate the song '{track_name}' from 1 to 5:", minvalue=1, maxvalue=5)
    if rating is None:
        messagebox.showwarning("Warning", "No rating provided.")
        return

    playlists = load_playlists_from_file()
    if not playlists:
        messagebox.showwarning("Warning", "No playlists found. Please create a playlist first.")
        return

    playlist_names = [p.name for p in playlists]
    selected_playlist = simpledialog.askstring("Select Playlist", f"Available playlists: {', '.join(playlist_names)}")

    if selected_playlist in playlist_names:
        for playlist in playlists:
            if playlist.name == selected_playlist:
                playlist.add_song(Song(track_name, track_url, description, rating))
                save_playlists_to_file(playlists)
                messagebox.showinfo("Success", f"Added '{track_name}' to playlist '{selected_playlist}' with a rating of {rating}.")
                return
    else:
        messagebox.showwarning("Warning", "Playlist not found.")


def create_new_playlist():
    playlist_name = simpledialog.askstring("Create Playlist", "Enter the name of the new playlist:")
    if playlist_name:
        playlists = load_playlists_from_file()
        new_playlist = Playlist(playlist_name)
        playlists.append(new_playlist)
        save_playlists_to_file(playlists)
        messagebox.showinfo("Success", f"Playlist '{playlist_name}' created successfully.")


def view_playlist():
    playlists = load_playlists_from_file()
    if not playlists:
        messagebox.showinfo("Info", "No playlists found.")
        return

    playlist_names = [p.name for p in playlists]
    selected_playlist_name = simpledialog.askstring("View Playlist", f"Available playlists: {', '.join(playlist_names)}")

    for playlist in playlists:
        if playlist.name == selected_playlist_name:
            song_list = playlist.list_songs()
            messagebox.showinfo(f"Playlist: {selected_playlist_name}", song_list)
            return
    messagebox.showwarning("Warning", "Playlist not found.")

def show_filtered_artists():
    global artist_data 
    search_text = artist_search_entry.get().strip().lower()
    if not search_text:
        messagebox.showinfo("Info", "Please enter a search term.")
        return
    
    filtered_artists = [artist for artist in artist_data if search_text in artist['name'].lower()]
    
    artist_data = filtered_artists

    artists_list.delete(0, tk.END)

    if filtered_artists:
        for idx, artist in enumerate(filtered_artists, start=1):
            artist_name = artist['name']
            artists_list.insert(tk.END, f"{idx}. {artist_name}")
    else:
        messagebox.showinfo("Info", f"No artists found matching '{search_text}'.")


def main():
    global artists_list, tracks_list, artist_search_entry

    root = tk.Tk()
    root.title("Musical Box")
    root.geometry("600x600")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill="both")

    tab_lastfm = ttk.Frame(notebook)
    tab_playlist = ttk.Frame(notebook)

    notebook.add(tab_lastfm, text="View")
    notebook.add(tab_playlist, text="Playlists Manager")

    tk.Label(tab_lastfm, text="Top Artists", font=("Arial", 14, "bold")).pack(pady=10)

    
    search_frame = tk.Frame(tab_lastfm)
    search_frame.pack(pady=5)

    tk.Label(search_frame, text="Search Artists:").pack(side=tk.LEFT, padx=5)
    artist_search_entry = tk.Entry(search_frame, width=20)
    artist_search_entry.pack(side=tk.LEFT, padx=5)
    tk.Button(search_frame, text="Search", command=show_filtered_artists).pack(side=tk.LEFT, padx=5)

    artists_list = tk.Listbox(tab_lastfm, width=50, height=10)
    artists_list.pack(pady=5)
    artists_list.bind("<<ListboxSelect>>", show_top_tracks)

    tk.Button(tab_lastfm, text="Load Top Artists", command=show_top_artists).pack(pady=10)
    tk.Button(tab_lastfm, text="Add Music to Playlist", command=add_track_to_playlist).pack(pady=10)

    tk.Button(tab_playlist, text="Create New Playlist", command=create_new_playlist).pack(pady=10)
    tk.Button(tab_playlist, text="View Playlist", command=view_playlist).pack(pady=10)

    tk.Label(tab_lastfm, text="Top Tracks", font=("Arial", 14, "bold")).pack(pady=10)
    tracks_list = tk.Listbox(tab_lastfm, width=50, height=10)
    tracks_list.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()