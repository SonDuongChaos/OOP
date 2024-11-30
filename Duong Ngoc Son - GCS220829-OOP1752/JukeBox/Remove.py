import tkinter as tk
from tkinter import messagebox

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
        self.songs = [song for song in self.songs if song.title != song_title]

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
        messagebox.showerror("Error", "No playlists file found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading playlists: {e}")
    return playlists

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

class PlaylistManager:
    def __init__(self, root):
        self.root = root
        self.playlists = load_playlists_from_file()
        self.selected_playlist = None

        self.setup_ui()

    def setup_ui(self):
        self.root.title("Musical Box")
        self.root.geometry("600x500")

        tk.Label(self.root, text="Playlists").pack()
        self.playlist_listbox = tk.Listbox(self.root, height=10, width=50)
        self.playlist_listbox.pack(pady=10)
        self.playlist_listbox.bind("<<ListboxSelect>>", self.on_playlist_select)

        tk.Label(self.root, text="Songs").pack()
        self.song_listbox = tk.Listbox(self.root, height=10, width=50)
        self.song_listbox.pack(pady=10)

        self.remove_playlist_button = tk.Button(self.root, text="Remove playlist", command=self.remove_playlist, state=tk.DISABLED)
        self.remove_playlist_button.pack(pady=10)

        self.remove_song_button = tk.Button(self.root, text="Remove music", command=self.remove_song, state=tk.DISABLED)
        self.remove_song_button.pack(pady=10)

        self.load_playlists_into_listbox()

    def load_playlists_into_listbox(self):
        self.playlist_listbox.delete(0, tk.END)
        for playlist in self.playlists:
            self.playlist_listbox.insert(tk.END, playlist.name)

    def on_playlist_select(self, event):
        selection = self.playlist_listbox.curselection()
        if not selection:
            return
        selected_index = selection[0]
        self.selected_playlist = self.playlists[selected_index]

        self.song_listbox.delete(0, tk.END)
        for song in self.selected_playlist.songs:
            self.song_listbox.insert(tk.END, song.title)

        self.remove_playlist_button.config(state=tk.NORMAL)
        self.remove_song_button.config(state=tk.NORMAL if self.selected_playlist.songs else tk.DISABLED)

    def remove_playlist(self):
        if not self.selected_playlist:
            return
        playlist_name = self.selected_playlist.name
        self.playlists.remove(self.selected_playlist)
        save_playlists_to_file(self.playlists)
        self.load_playlists_into_listbox()
        self.song_listbox.delete(0, tk.END)
        messagebox.showinfo("Success", f"Playlist '{playlist_name}' removed successfully!")
        self.remove_playlist_button.config(state=tk.DISABLED)
        self.remove_song_button.config(state=tk.DISABLED)

    def remove_song(self):
        selection = self.song_listbox.curselection()
        if not selection or not self.selected_playlist:
            return
        selected_index = selection[0]
        song_title = self.selected_playlist.songs[selected_index].title
        self.selected_playlist.remove_song(song_title)
        save_playlists_to_file(self.playlists)
        self.song_listbox.delete(selected_index)
        messagebox.showinfo("Success", f"Song '{song_title}' removed successfully!")

def main():
    root = tk.Tk()
    app = PlaylistManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
