import time
time.sleep(20)
import modules.mysql as mysql
import modules.webhooks as webhooks
import modules.steamapi as steam
import modules.secrets as secrets
import modules.imagegenerator as ig



def main():
    mysql.populatedb()
    listOfFriendSteamIds = secrets.load_secret_config("players")["STEAM_IDS"]
    while True:
        for steamId in listOfFriendSteamIds:
            matchData = steam.get_most_recent_match(steamId)
            if matchData:
                print("game found!")
                for player in matchData.players:
                    playerMetaInfo = steam.get_player_info(player.account_id+76561197960265728)
                    if playerMetaInfo != None:
                        mysql.insert_into_db("INSERT IGNORE INTO players (id, dota2_id, name, avatar) VALUES (%s,%s, %s, %s)",[(playerMetaInfo["steamid"],player.account_id,playerMetaInfo["personaname"],playerMetaInfo["avatar"])])
                    else:
                        mysql.insert_into_db("INSERT IGNORE INTO players (dota2_id) VALUES (%s)",[tuple([player.account_id])])
                mysql.insert_match_into_db(matchData)
                image = ig.create_image(matchData)
                webhooks.update_discord(matchData,image)
            else:
                pass
        time.sleep(120)

if __name__ == "__main__":
    main()