import requests
import mysql.connector
from modules.match import Match
import modules.steamapi as dota2
import modules.secrets as secrets

databaseInfo = secrets.load_secret_config("database")
mydb = mysql.connector.connect(host=databaseInfo["MYSQL_HOST"],database=databaseInfo["MYSQL_DATABASE"],user=databaseInfo["MYSQL_USER"],password=databaseInfo["MYSQL_PASSWORD"],port=databaseInfo["MYSQL_PORT"])

def populatedb() -> None:
    db_cursor = mydb.cursor()
    try:
        items = requests.get("https://raw.githubusercontent.com/odota/dotaconstants/master/build/items.json").json()
        insertItems = []
        for itemName,itemInfo in items.items():
            insertItems.append((itemInfo["id"],itemName,itemInfo["img"].replace("?","").split("t=")[0]))
        insertItems.append((0,None,None))
        db_cursor.executemany("INSERT IGNORE INTO items (id, name, img) VALUES (%s, %s, %s)",insertItems)
        mydb.commit()
    except Exception as e:
        print(f"unable to popualate database with items: {e}")
    try:
        heroes = requests.get("https://raw.githubusercontent.com/odota/dotaconstants/master/build/heroes.json").json()
        insertHeroes = []
        for heroInfo in heroes.values():
            insertHeroes.append((heroInfo["id"],heroInfo["localized_name"],heroInfo["img"].replace("?","")))
        db_cursor.executemany("INSERT IGNORE INTO heroes (id, name, img) VALUES (%s, %s, %s)",insertHeroes)
        mydb.commit()
    except Exception as e:
        print(f"unable to popualate database with heroes: {e}")
    """
    try:
        players = [(76561198070542219, "TheLiarGod"),(76561198050050401,"TheZoom")]
        db_cursor.executemany("INSERT IGNORE INTO players (id, name) VALUES (%s, %s)",players)
        mydb.commit()
    except Exception as e:
        print(f"unable to popualate database with players: {e}")
    """
    db_cursor.close()


def insert_into_db(query,value):
    db_cursor = mydb.cursor()
    db_cursor.executemany(query,value)
    mydb.commit()
    db_cursor.close()


def select_db(query) -> list:
    db_cursor = mydb.cursor()
    db_cursor.execute(query)
    if db_cursor.with_rows:
        rows = db_cursor.fetchall()
    else:
        rows = []
    db_cursor.close()
    return rows

def insert_match_into_db(match_data):
    db_cursor = mydb.cursor()

    query = """
    INSERT IGNORE INTO matches (radiant_win, duration, pre_game_duration, start_time, id, match_seq_num, 
                            tower_status_radiant, tower_status_dire, barracks_status_radiant, barracks_status_dire, 
                            lobby_type, leagueid, game_mode, radiant_score, dire_score)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    value = [(
        match_data.radiant_win, match_data.duration, match_data.pre_game_duration, match_data.start_time, match_data.match_id,
        match_data.match_seq_num, match_data.tower_status_radiant, match_data.tower_status_dire, match_data.barracks_status_radiant,
        match_data.barracks_status_dire, match_data.lobby_type, match_data.leagueid, match_data.game_mode, match_data.radiant_score, match_data.dire_score
    )]
    print(value)
    db_cursor.executemany(query,value)
    mydb.commit()
    
    query = """
    INSERT IGNORE INTO match_players (account_id, match_id, player_slot, team_number, team_slot, hero_id, hero_variant,
                               item_0, item_1, item_2, item_3, item_4, item_5,
                               backpack_0, backpack_1, backpack_2, item_neutral,
                               kills, deaths, assists, leaver_status,
                               last_hits, denies, gold_per_min, xp_per_min,
                               level, net_worth, aghanims_scepter, aghanims_shard, moonshard,
                               hero_damage, tower_damage, hero_healing,
                               gold, gold_spent, scaled_hero_damage, scaled_tower_damage, scaled_hero_healing)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    match_players = []
    for player in match_data.players:
        match_players.append((
            player.account_id,
            match_data.match_id,
            player.player_slot,
            player.team_number,
            player.team_slot,
            player.hero_id,
            player.hero_variant,
            player.item_0,
            player.item_1,
            player.item_2,
            player.item_3,
            player.item_4,
            player.item_5,
            player.backpack_0,
            player.backpack_1,
            player.backpack_2,
            player.item_neutral,
            player.kills,
            player.deaths,
            player.assists,
            player.leaver_status,
            player.last_hits,
            player.denies,
            player.gold_per_min,
            player.xp_per_min,
            player.level,
            player.net_worth,
            player.aghanims_scepter,
            player.aghanims_shard,
            player.moonshard,
            player.hero_damage,
            player.tower_damage,
            player.hero_healing,
            player.gold,
            player.gold_spent,
            player.scaled_hero_damage,
            player.scaled_tower_damage,
            player.scaled_hero_healing
        ))
    db_cursor.executemany(query,match_players)
    mydb.commit()
    
    query = f"""
        UPDATE matches
        SET player1_id = %s, player2_id = %s, player3_id = %s, player4_id = %s, player5_id = %s,
            player6_id = %s, player7_id = %s, player8_id = %s, player9_id = %s, player10_id = %s
        WHERE id = {match_data.match_id}
        """

    db_cursor.close()