# Import the tkinter library to create graphical user interfaces
import tkinter as tk

# Import font_manager and other supporting files or functions
import font_manager as fonts  # Configure fonts (defined in the font_manager file)
import expand_search  # Manage expanded search functionality
from expand_search import Playlist, Song  # Import Playlist and Song classes from expand_search
from song_player import MusicPlayer  # Import the music player class
from update_list import main as edit_playlist  # Import the playlist update function and rename it to edit_playlist
from Remove import main  # Import the function to remove playlists or songs

# Define a function to save the state and exit the program
def save_and_quit():
    # Update the status
    status_lbl.configure(text="Saving and quitting...")
    # Close the main window
    window.destroy()

# Define a function to handle the event when the "Start" button is clicked
def main_button_clicked():
    # Hide the main button
    main_btn.grid_forget()
    # Update the status
    status_lbl.configure(text="Start was clicked!")
    
    # Create and display a "Playlists" button to manage playlists
    add_song_button = tk.Button(window, text="Playlists", command=list_clicked)
    add_song_button.grid(row=2, column=1, padx=10, pady=10)
    
    # Create and display a "Play music" button to play songs
    play_song_button = tk.Button(window, text="Play music", command=playsongs_clicked)
    play_song_button.grid(row=3, column=1, padx=10, pady=10)

    # Create and display an "Update information playLists" button to update playlists
    update_music = tk.Button(window, text="Update information playLists", command=update_music_clicked)
    update_music.grid(row=4, column=1, padx=10, pady=10)
    
    # Create and display a "Remove music or playlists" button to delete songs/playlists
    remove_button = tk.Button(window, text="Remove music or playlists", command=remove_clicked)
    remove_button.grid(row=5, column=1, padx=10, pady=10)
    
    # Create and display a "Save and quit" button to save and exit
    save_quit_button = tk.Button(window, text="Save and quit", command=save_and_quit)
    save_quit_button.grid(row=6, column=1, padx=10, pady=10)

# Define the function to handle the event when the "Playlists" button is clicked
def list_clicked():
    # Call the main function from expand_search to display the playlists
    expand_search.main()

# Define the function to handle the event when the "Play music" button is clicked
def playsongs_clicked():
    # Update the status
    status_lbl.configure(text="Play music button was clicked!")
    # Create a new window for playing music
    root = tk.Tk()
    # Initialize the music player
    music_player = MusicPlayer(root)
    # Run the main loop for the new window
    root.mainloop()

# Define the function to handle the event when the "Update information playLists" button is clicked
def update_music_clicked():
    # Update the status
    status_lbl.configure(text="Update music button was clicked!")
    # Call the function to update playlists
    edit_playlist()
    
# Define the function to handle the event when the "Remove music or playlists" button is clicked
def remove_clicked():
    # Update the status
    status_lbl.configure(text="Remove music button was clicked!")
    # Call the function to remove items
    main()

# Initialize the main window
window = tk.Tk()
# Set the window size
window.geometry("520x200")
# Set the window title
window.title("Musical Box")
# Set the background color of the window
window.configure(bg="palegreen")

# Configure fonts
fonts.configure()

# Add a header label to the window
header_lbl = tk.Label(window, text="Welcome to the Musical Box app")
header_lbl.grid(row=0, column=0, columnspan=3, padx=15, pady=10)

# Create and display the "Start" button on the main window
main_btn = tk.Button(window, text="Start", command=main_button_clicked)
main_btn.grid(row=1, column=1, padx=10, pady=10)

# Add a status label to the window
status_lbl = tk.Label(window, bg='palegreen', text="", font=("Helvetica", 10))
status_lbl.grid(row=7, column=1, columnspan=2, padx=10, pady=10)

# Run the tkinter main loop
window.mainloop()
