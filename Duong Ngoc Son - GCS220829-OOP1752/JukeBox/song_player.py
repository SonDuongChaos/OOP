import tkinter as tk
from tkinter import messagebox
import webbrowser

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

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.playlists = self.load_playlists_from_file()
        self.selected_playlist = None
        self.selected_song = None
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Musical Box")
        self.root.geometry("600x500")

        tk.Label(self.root, text="Playlists").pack()
        self.playlist_listbox = tk.Listbox(self.root, height=10, width=50)
        self.playlist_listbox.pack(pady=10)
        self.playlist_listbox.bind("<<ListboxSelect>>", self.on_playlist_select)

        tk.Label(self.root, text="Music").pack()
        self.song_listbox = tk.Listbox(self.root, height=10, width=50)
        self.song_listbox.pack(pady=10)

        self.play_button = tk.Button(self.root, text="Play", command=self.play_selected_song, state=tk.DISABLED)
        self.play_button.pack(pady=20)

        self.load_playlists_into_listbox()

    def load_playlists_from_file(self):
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
                        try:
                            title = line
                            url = lines[i+1].strip()
                            description = lines[i+2].strip()
                            rating = int(lines[i+3].strip())
                            current_playlist.add_song(Song(title, url, description, rating))
                            i += 3
                        except IndexError:
                            messagebox.showwarning("Warning", "Playlist file is improperly formatted.")
                            break
                    i += 1
                if current_playlist:
                    playlists.append(current_playlist)
        except FileNotFoundError:
            messagebox.showerror("Error", "No playlists file found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading playlists: {e}")
        return playlists

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
        
        self.play_button.config(state=tk.NORMAL if self.selected_playlist.songs else tk.DISABLED)

    def play_selected_song(self):
        selection = self.song_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a music to play.")
            return
        
        selected_index = selection[0]
        self.selected_song = self.selected_playlist.songs[selected_index]

        if self.selected_song.url:
            try:
                webbrowser.open(self.selected_song.url)
                messagebox.showinfo("Now Playing", f"Opening: {self.selected_song.title} in your browser")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open the song URL: {e}")
        else:
            messagebox.showwarning("Warning", "This music does not have a valid URL.")

def main():
    root = tk.Tk()
    music_player = MusicPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
