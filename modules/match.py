from modules.player import Player
class Match:
    def __init__(self,data) -> None:
        self.players = []
        for players in data["players"]:
            self.players.append(Player(players))
        self.radiant_win=data['radiant_win']
        self.duration=data['duration']
        self.pre_game_duration=data['pre_game_duration']
        self.start_time=data['start_time']
        self.match_id=data['match_id']
        self.match_seq_num=data['match_seq_num']
        self.tower_status_radiant=data['tower_status_radiant']
        self.tower_status_dire=data['tower_status_dire']
        self.barracks_status_radiant=data['barracks_status_radiant']
        self.barracks_status_dire=data['barracks_status_dire']
        self.cluster=data['cluster']
        self.first_blood_time=data['first_blood_time']
        self.lobby_type=data['lobby_type']
        self.human_players=data['human_players']
        self.leagueid=data['leagueid']
        self.game_mode=data['game_mode']
        self.flags=data['flags']
        self.engine=data['engine']
        self.radiant_score=data['radiant_score']
        self.dire_score=data['dire_score']