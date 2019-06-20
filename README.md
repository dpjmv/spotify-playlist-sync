# Spotify Playlist Sync

Syncing my spotify playlists

To use this script, you must specify a user to interact with.
This can be achieved by providing the username as an arguemnt or through
the SPFY_PL_SYNC_USERNAME environment variable.

You will also need to change the name of the three variables:

- temp_name (string)
- specific_names (list of string)
- mega_name (string)

in order for them to suit the name of your playlists. You can find these
at the top of the main() function.

Flow:
If any music that is in a specific playlist is aslo in origin. It
shall be copied into mega and removed from origin.

Why:
Because I add the new musics I find into a temporary playlist, and if
I am not borded of hearing them after three times, I add them to a specific
playlist based on the type of music and a global playlist joining them all.

Note:
You will need to register the app to get an api key for Spotify. When
first using the script, you will be prompted to grant access to the app
in your browser.