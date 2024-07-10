import requests
import modules.mysql as mysql
import time
from modules.match import Match
import modules.secrets as secrets

apiToken = secrets.load_secret_config("keys")["STEAM_KEY"]

# Return Most Recent Match
def get_match_history(steamid) -> dict:
    try:   
        response = requests.get(f"https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/v1/?account_id={steamid}&key={apiToken}")
        if response.status_code == 200:
            return response.json()["result"]["matches"][0]
        else:
            print(f"Not status code 200: {response.json()}")
            return False
    except Exception as e:
        print(f"Warning: {e}")

# Returns Match Data From match_seq_num
def get_match_data(matchSeqId) -> dict:
    try:   
        response = requests.get(f"https://api.steampowered.com/IDOTA2Match_570/GetMatchHistoryBySequenceNum/v1/?start_at_match_seq_num={matchSeqId}&key={apiToken}&matches_requested=1")
        if response.status_code == 200:
            return response.json()["result"]["matches"][0]
        else:
            print(f"Not status code 200: {response.json()}")
            return False
    except Exception as e:
        print(f"Warning: {e}")

# If the game started in the last 2 hrs, we insert it into the db + return the match data
def get_most_recent_match(steamid) -> Match:
    matchHistory = get_match_history(steamid)
    if time.time() - (60*60*48) <= matchHistory["start_time"] and len(mysql.select_db(f"SELECT id FROM matches WHERE id = {matchHistory['match_id']}")) == 0:
        match_data = Match(get_match_data(matchHistory["match_seq_num"]))
        return match_data
    else:
        return False

# Gets a players meta data outside of the game such as avatar, name, and steamid
def get_player_info(steamId):
    try:   
        response = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?steamids={steamId}&key={apiToken}")
        if response.status_code == 200:
            if len(response.json()["response"]["players"]) == 1:
                player = response.json()["response"]["players"][0]
                return player
            else:
                print(f"Could not find player:{steamId}")
                return None
        else:
            print(f"Not status code 200: {response.json()}")
            return None
    except Exception as e:
        print(f"Warning: {e}")
     
