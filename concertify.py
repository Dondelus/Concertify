from typing import Tuple
from eventbrite import Eventbrite
import pprint
import spotipy
import spotipy.util as util

import config


def setup_spotify():
    username = input("Please enter your spotify username: ")
    
    token = util.prompt_for_user_token(
        username=username,
        scope=config.SCOPES,
        client_id=config.spotify_client_id,
        client_secret=config.spotify_client_secret,
        redirect_uri='https://localhost/callback'
    )
    spotify = spotipy.Spotify(auth=token)
    
    return spotify


def setup_eventbrite():
	eventbrite = Eventbrite(config.eventbrite_client_id)

	return eventbrite


def get_all_user_follows(spotify, limit=50) -> list:
    '''
    Return a list of all artists followed by the current user.
    '''
    artists, next_id = extract_artist_names(spotify.current_user_followed_artists(limit))

    while next_id is not None:
        next_batch, next_id = extract_artist_names(spotify.current_user_followed_artists(limit, next_id))
        artists.extend(next_batch)

    return artists


def extract_artist_names(bulk_artist_data) -> Tuple[list, str]:
    '''
    Given a bulk_artist_data dict, return a list of artist names and the next artist_id to retrieve by.
    '''
    artists = [artist['name'] for artist in bulk_artist_data['artists']['items']]
    next_artist_id = bulk_artist_data['artists']['cursors']['after']

    return artists, next_artist_id


def get_concerts(eventbrite, artists) -> list:
	concerts = []

	for artist in artists:
		concerts.append(eventbrite.event_search(q=artist))

	return concerts


if __name__ == "__main__":
    sp = setup_spotify()
    eb = setup_eventbrite()