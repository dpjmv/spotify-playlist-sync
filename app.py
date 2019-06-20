import spotipy
import sys
import spotipy.util as util
import os


def connectToSpotify(username):
    """
    Default constructor

    :param username: 
        Username of the user to interact with.
    
    :returns:
        A spotipy.Spotify object that can then be used to interact
        with the Spotify Web API
    """
    scopes = 'playlist-read-private playlist-read-collaborative ' + \
        'playlist-modify-public playlist-modify-private'

    token = util.prompt_for_user_token(username, scopes)
    if not token:
        print(f"No token for user {username}")
        sys.exit()
    
    return spotipy.Spotify(auth=token)


def getPlaylists(sp, username, offset=0):
    """
    Retrieves all the playlists a user has

    :param sp:
        A spotipy.Spotify object to be used for the request.

    :param username:
        The username of the user who's playlists you want the retrieve.
    
    :param offset:
        Do not worry about this parameter, it is used for recursion.
    
    :returns:
        A dict containing all of the user's playlists.
    """
    limit = 50

    api_response = sp.user_playlists(username, limit, offset)

    playlists = [x for x in api_response["items"]]

    if api_response["total"] > limit + offset:
        next_playlists = getPlaylists(sp, username, offset + limit)
        for playlist in next_playlists:
            playlists.append(playlist)
    
    return playlists


def getTrackIds(sp, username, playlist, offset=0):
    """
    Returns the ids of the tracks contained in a playlist

    :param sp:
        A spotipy.Spotify object to be used for the request.

    :param username:
        The username of the user who's playlists you want the retrieve.

    :param playlist:
        Name of the playlist from wich the tracks are retrieved.

    :param offset:
        Do not worry about this parameter, it is used for recursion.
    
    :returns:
        A list containing all the ids of the tracks that are in the playlist.
    """
    limit = 100
    fields = "items(track(id)), total"

    api_response = sp.user_playlist_tracks(username,
        playlist["id"], fields, limit=limit, offset=offset)

    track_ids = [x["track"]["id"] for x in api_response["items"]]

    if api_response["total"] > limit + offset:
        next_page = getTrackIds(sp, username, playlist, offset + limit)
        for item in next_page:
            track_ids.append(item)
    
    return track_ids


def main():
    """
    Main function
    
    To use this script, you must specify a user to interact with.
    This can be achieved by providing the username as an arguemnt or through
    the SPFY_PL_SYNC_USERNAME environment variable.

    You will also need to change the name of the three variables:
        - origin_name (string)
        - specific_names (list of strings)
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
    """
    origin_name = "Purgatoire"
    specific_names = ["Rock", "Classique", "Rap",
        "Chiant", "Poubelle", "Trad"]
    mega_name = "MEGA PLAYLIST"

    # Retrieve username
    username = os.getenv("SPFY_PL_SYNC_USERNAME")

    if username:
        pass
    elif len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print(f"Usage: {sys.argv[0]} username")
        sys.exit()

    # Connect to spotify
    sp = connectToSpotify(username)

    # Get the user's playlists
    playlists = getPlaylists(sp, username)

    # Pick out the ones we need
    specific_pls = []
    for playlist in playlists:
        if playlist["name"] == origin_name:
            origin_pl = playlist
        elif playlist["name"] == mega_name:
            mega_pl = playlist
        elif playlist["name"] in specific_names:
            specific_pls.append(playlist)
    
    # Get tracks
    origin_tracks = getTrackIds(sp, username, origin_pl)

    specific_tracks = []
    for pl in specific_pls:
        for track in getTrackIds(sp, username, pl):
            specific_tracks.append(track)
    
    # Pick out the ones recently added to specific playlists
    new_tracks = list(set(origin_tracks).intersection(specific_tracks))

    if new_tracks:
        # Add them to mega
        print(new_tracks)
        sp.user_playlist_add_tracks(username, mega_pl["id"], new_tracks)

        # Remove them from origin
        sp.user_playlist_remove_all_occurrences_of_tracks(username,
            origin_pl["id"], new_tracks)

        print(f"Handled {len(new_tracks)} new tracks.")
    else:
        print("Nothing done.")


if __name__ == "__main__":
    main()