import spotipy as spotify
import requests as re
from webcolors import rgb_to_name
import sys
import urllib.parse as urlparse
from simplejson.errors import JSONDecodeError
from requests.exceptions import JSONDecodeError as RJSONDecodeError
from json import dumps, dump


class colorify:

    def __init__(self,  client_token, sha_hash="411f31a2759bcb644bf85c58d2f227ca33a06d30fbb0b49d0f6f264fda05ecd8", public_api_client_id="01800d9a6c004dc9863ae48feb01af86", public_api_client_secret="6c6d109a079e4565bdbe9a85befd6edd", spotify_scopes=None) -> None:
        self.sha_hash = sha_hash
        self.scopes = spotify_scopes
        self.default_useragent = "Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0"
        self.refresh_client_auth()

        self.client_token = client_token
        self.authmanager = spotify.SpotifyOAuth(
            client_secret=public_api_client_secret, client_id=public_api_client_id, redirect_uri="http://localhost:4002",scope=self.scopes)
        c0de = self.authmanager.get_authorization_code(),
        self.public_api_session = spotify.Spotify(
            auth=self.authmanager.get_access_token(c0de)['access_token'])
        
        pass
    def refresh_public_api_token(self):
        c0de = self.authmanager.get_authorization_code()

        self.public_api_session = spotify.Spotify(
            auth=self.authmanager.get_access_token(c0de, as_dict=False,check_cache=True))
        
    def refresh_client_auth(self):
        self.client_auth=("Bearer "+re.get("https://open.spotify.com/get_access_token",
                                             headers={
                                                 'User-Agent': self.default_useragent,
                                                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                                                 'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
                                                 'DNT': '1',
                                                 'Upgrade-Insecure-Requests': '1',
                                                 'Sec-Fetch-Dest': 'document',
                                                 'Sec-Fetch-Mode': 'navigate',
                                                 'Sec-Fetch-Site': 'none','Sec-Fetch-User': '?1','Connection': 'keep-alive','Alt-Used': 'open.spotify.com','Pragma': 'no-cache',
                                                 'Cache-Control': 'no-cache',
                                             }
                                             ).json()['accessToken'])
        return self.client_auth
    def rgbify(self, hexcode):
        return tuple(int(hexcode.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

    def get_color(self, _track) -> dict:

        album_id = self.public_api_session.track(_track)['album']['id']
 
        base_url = f"https://api-partner.spotify.com/pathfinder/v1/query"
       
        params = {
            'operationName': 'getAlbumMetadata',
            'variables': dumps({"uri": "spotify:album:{0}".format(album_id), "locale": ""}),
            'extensions': dumps({"persistedQuery": {"version": 1, "sha256Hash": self.sha_hash}}),
        }
        try:
            rq = re.get(base_url, headers={
                "User-Agent": self.default_useragent,
                "Accept": "application/json",
                'Referer': 'https://open.spotify.com/',
                'spotify-app-version': '1.2.0.550.g8c3f5655',
                "Accept-Language": "es",
                "app-platform": "WebPlayer",
                "spotify-app-version": "1.1.96.83.g8ad99f81",
                "content-type": "application/json;charset=UTF-8",
                "client-token": self.client_token,
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                "Sec-Fetch-Site": "same-site",
                "authorization": self.client_auth
            }, params=params)
            jsn = rq.json()
        except (JSONDecodeError, RJSONDecodeError) as e:
             rq = re.get(base_url, headers={
                "User-Agent": self.default_useragent,
                "Accept": "application/json",
                'Referer': 'https://open.spotify.com/',
                'spotify-app-version': '1.2.0.550.g8c3f5655',
                "Accept-Language": "es",
                "app-platform": "WebPlayer",
                "spotify-app-version": "1.1.96.83.g8ad99f81",
                "content-type": "application/json;charset=UTF-8",
                "client-token": self.client_token,
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                "Sec-Fetch-Site": "same-site",
                "authorization": self.refresh_client_auth()
             }, params=params)
             jsn = rq.json()
        dump(fp=open("daa.json","w"), obj=jsn)
        data = (jsn['data']['albumUnion']['coverArt']
                ['extractedColors']['colorRaw']['hex'])
        return dict(hexadecimal=data.replace("#",""),rgb=self.rgbify(data),rgb_as_string=f'RGB({", ".join(list(map(str, self.rgbify(data))))})' )
