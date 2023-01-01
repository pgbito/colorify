import tinytuya

import time
from colorsys import rgb_to_hsv
import os
if os.getlogin()=="pgbit" and os.name == "nt": # ignore this shit 
  os.chdir(os.path.join("M:\\", "mpriscolorify"))

from colorify import colorify
d = tinytuya.BulbDevice('1262084540f52024901d',
                        '192.168.0.4', '8ee4ff2101bcf00e')

d.set_version(3.3)

NoneType=None.__class__

color = colorify(
    client_token=input("Enter your client token from an existing open.spotify.com client").strip(),
    spotify_scopes="user-read-playback-state")
previous_track = None
print("Entering main loop.")
while True:
    
    try:
        track = color.public_api_session.current_playback()
    except Exception:
        color.refresh_client_auth()
        track = color.public_api_session.current_playback()
    if track is None:
        continue

    rawtrack = track.pop('item')
    try:
        
        
        name = rawtrack.pop('name')
        artists = " ,".join(
            list(map(lambda artist: artist.pop('name'), rawtrack.get('artists'))))
    except AttributeError:
        continue
    current_track='Now playing {title} by {artist}'.format(title=name, artist=artists)
    if current_track == previous_track:
        continue
    is_playing = track.pop('is_playing')
    playlist = track.pop("context")
    progress_ms = track.pop('progress_ms')
    uri = rawtrack.pop('uri')
    full_ms = rawtrack.pop('duration_ms')    
    
    del track
    del rawtrack  # pop name, artist names, popularity for logging
    remaining_ms = full_ms-progress_ms
    
    color_data = color.get_color(
        uri)
    previous_track = current_track
   
  
    hexvalue = color_data.get("hexadecimal")+ "00000000" 

  
    
    payload = d.generate_payload(tinytuya.CONTROL,
                                 {
                                     d.DPS_INDEX_MODE[d.bulb_type]: d.DPS_MODE_COLOUR,
                                     d.DPS_INDEX_COLOUR[d.bulb_type]: hexvalue,
                                 },)

    color_data = d._send_receive(payload)
    print(previous_track)
    time.sleep(2.5)

    
