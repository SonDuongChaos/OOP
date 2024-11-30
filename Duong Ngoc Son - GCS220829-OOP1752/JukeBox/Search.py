import tkinter as tk
from tkinter import simpledialog, messagebox

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

    def search_song(self, query, search_by="title"):
        results = []
        for song in self.songs:
            if search_by == "title" and query.lower() in song.title.lower():
                results.append(song)
            elif search_by == "rating" and song.rating == int(query):
                results.append(song)
        return results


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
                    url = lines[i+1].strip()
                    description = lines[i+2].strip()
                    rating = int(lines[i+3].strip())
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


def search_song_in_playlists():
    playlists = load_playlists_from_file()
    if not playlists:
        messagebox.showwarning("Warning", "No playlists available.")
        return

    search_by = simpledialog.askstring("Search", "Search by:\n1. Title\n2. Rating\nEnter 1 or 2:")
    if search_by not in ["1", "2"]:
        messagebox.showwarning("Warning", "Invalid choice. Please enter 1 or 2.")
        return

    if search_by == "1":
        query = simpledialog.askstring("Search Query", "Enter title or a part of the title:")
        search_field = "title"
    elif search_by == "2":
        query = simpledialog.askstring("Search Query", "Enter rating (1-5):")
        if not query.isdigit() or not (1 <= int(query) <= 5):
            messagebox.showwarning("Warning", "Please enter a valid rating between 1 and 5.")
            return
        search_field = "rating"
    else:
        return

    if not query:
        messagebox.showwarning("Warning", "Search query cannot be empty.")
        return

    results = []

    for playlist in playlists:
        results.extend(playlist.search_song(query, search_field))

    if results:
        result_text = "\n".join([f"Title: {song.title}\nURL: {song.url}\nDescription: {song.description}\nRating: {song.rating}\n{'-'*30}"
                                 for song in results])
        messagebox.showinfo("Search Results", result_text)
    else:
        messagebox.showinfo("No Results", "No songs found matching your search query.")

def main():
    root = tk.Tk()
    root.title("Musical Box")
    root.geometry("400x200")

    search_button = tk.Button(root, text="Search for music by title or rating from playlists", command=search_song_in_playlists, width=40, height=2)
    search_button.pack(pady=60)

    root.mainloop()

if __name__ == "__main__":
    main()
