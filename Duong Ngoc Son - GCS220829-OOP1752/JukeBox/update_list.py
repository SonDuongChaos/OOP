import tkinter as tk
from tkinter import messagebox, simpledialog

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

    def update_playlist_name(self, new_name):
        self.name = new_name

    def update_song(self, song, field, new_value):
        if field == "title":
            song.title = new_value
        elif field == "url":
            song.url = new_value
        elif field == "description":
            song.description = new_value
        elif field == "rating":
            song.rating = int(new_value)

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
                elif line:  # If the line is not empty
                    title = line
                    url = lines[i + 1].strip()
                    description = lines[i + 2].strip()
                    rating = lines[i + 3].strip()
                    rating = int(rating) if rating.isdigit() else None
                    current_playlist.add_song(Song(title, url, description, rating))
                    i += 3
                i += 1
            if current_playlist:
                playlists.append(current_playlist)
    except FileNotFoundError:
        messagebox.showerror("Error", "Playlists file not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading playlists: {e}")
    return playlists

def save_playlists_to_file(playlists):
    try:
        with open("playlists.txt", "w") as file:
            for playlist in playlists:
                file.write(f"Playlist: {playlist.name}\n")
                for song in playlist.songs:
                    file.write(f"{song.title}\n{song.url}\n{song.description}\n{song.rating}\n")
                file.write("\n")
    except IOError as e:
        messagebox.showerror("Error", f"An error occurred while saving the playlists: {e}")

class PlaylistEditor:
    def __init__(self, root):
        self.root = root
        self.playlists = load_playlists_from_file()
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

        tk.Label(self.root, text="Songs").pack()
        self.song_listbox = tk.Listbox(self.root, height=10, width=50)
        self.song_listbox.pack(pady=10)
        self.song_listbox.bind("<<ListboxSelect>>", self.on_song_select)

        self.edit_button = tk.Button(self.root, text="Edit Music", command=self.edit_song, state=tk.DISABLED)
        self.edit_button.pack(pady=10)

        self.rename_playlist_button = tk.Button(self.root, text="Rename Playlists", command=self.rename_playlist, state=tk.DISABLED)
        self.rename_playlist_button.pack(pady=10)

        self.load_playlists_into_listbox()

    def load_playlists_into_listbox(self):
        self.playlist_listbox.delete(0, tk.END)
        for playlist in self.playlists:
            self.playlist_listbox.insert(tk.END, playlist.name)

    def load_songs_into_listbox(self):
        if self.selected_playlist:
            self.song_listbox.delete(0, tk.END)
            for song in self.selected_playlist.songs:
                self.song_listbox.insert(tk.END, song.title)

    def on_playlist_select(self, event):
        selection = self.playlist_listbox.curselection()
        if not selection:
            return
        selected_index = selection[0]
        self.selected_playlist = self.playlists[selected_index]
        self.load_songs_into_listbox()
        self.rename_playlist_button.config(state=tk.NORMAL)

    def on_song_select(self, event):
        selection = self.song_listbox.curselection()
        if not selection:
            return
        selected_index = selection[0]
        self.selected_song = self.selected_playlist.songs[selected_index]
        self.edit_button.config(state=tk.NORMAL)

    def edit_song(self):
        if not self.selected_song:
            messagebox.showwarning("Warning", "Please select a song to edit.")
            return

        options = ["title", "url", "description", "rating"]
        field_to_edit = simpledialog.askstring(
            "Edit Field", f"Choose a field to edit: {', '.join(options)}"
        )

        if field_to_edit not in options:
            messagebox.showwarning("Warning", "Invalid field selected.")
            return

        current_value = getattr(self.selected_song, field_to_edit, "Not set")
        new_value = simpledialog.askstring(
            f"Edit {field_to_edit.capitalize()}",
            f"Current {field_to_edit}: {current_value}\nEnter new value:",
        )

        if new_value:
            if field_to_edit == "rating":
                try:
                    new_value = int(new_value)
                    if not (1 <= new_value <= 5):
                        raise ValueError
                except ValueError:
                    messagebox.showwarning("Warning", "Rating must be a number between 1 and 5.")
                    return

            self.selected_playlist.update_song(self.selected_song, field_to_edit, new_value)
            save_playlists_to_file(self.playlists)
            self.load_songs_into_listbox()
            messagebox.showinfo("Success", "Song updated successfully!")

    def rename_playlist(self):
        if not self.selected_playlist:
            messagebox.showwarning("Warning", "Please select a playlist to rename.")
            return

        new_name = simpledialog.askstring("Rename Playlist", f"Current name: {self.selected_playlist.name}\nEnter new name:")
        if new_name:
            self.selected_playlist.update_playlist_name(new_name)
            save_playlists_to_file(self.playlists)
            self.load_playlists_into_listbox()
            messagebox.showinfo("Success", "Playlist renamed successfully!")

def main():
    root = tk.Tk()
    app = PlaylistEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
