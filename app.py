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

    username = username
    token = util.prompt_for_user_token(username, scopes)
    if not token:
        print(f"No token for user {username}")
        sys.exit()
    
    return spotipy.Spotify(auth=token)


def main():
    """
    Main function
    
    To use this script, you must specify a user to interact with.
    This can be achieved by providing the username as an arguemnt or through
    the SPFY_PL_SYNC_USERNAME environment variable.
    """

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

    # Print the user's playlists
    print(sp.user_playlists(username))


if __name__ == "__main__":
    main()