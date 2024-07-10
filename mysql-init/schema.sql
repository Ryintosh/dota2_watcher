CREATE DATABASE IF NOT EXISTS dota2;
USE dota2;
CREATE TABLE heroes (
    id int,
    name VARCHAR(255),
    img VARCHAR(255),
    PRIMARY KEY (ID)
);
CREATE TABLE items (
    id int,
    name VARCHAR(255),
    img VARCHAR(255),
    PRIMARY KEY (ID)
);
CREATE TABLE players (
    id BIGint,
    dota2_id BIGint,
    name VARCHAR(255),
    avatar VARCHAR(255),
    PRIMARY KEY (ID)
);

ALTER TABLE players
ADD CONSTRAINT unique_account_id UNIQUE (dota2_id);

CREATE TABLE matches (
    id BIGINT PRIMARY KEY,
    radiant_win BOOLEAN,
    duration INT,
    pre_game_duration INT,
    start_time INT,
    match_seq_num BIGINT,
    tower_status_radiant INT,
    tower_status_dire INT,
    barracks_status_radiant INT,
    barracks_status_dire INT,
    lobby_type INT,
    leagueid INT,
    game_mode INT,
    radiant_score INT,
    dire_score INT
);
CREATE TABLE match_players (
    id INT PRIMARY KEY AUTO_INCREMENT,
    match_id BIGINT,
    account_id BIGINT,
    player_slot INT,
    team_number INT,
    team_slot INT,
    hero_id INT,
    hero_variant INT,
    item_0 INT,
    item_1 INT,
    item_2 INT,
    item_3 INT,
    item_4 INT,
    item_5 INT,
    backpack_0 INT,
    backpack_1 INT,
    backpack_2 INT,
    item_neutral INT,
    kills INT,
    deaths INT,
    assists INT,
    leaver_status INT,
    last_hits INT,
    denies INT,
    gold_per_min INT,
    xp_per_min INT,
    level INT,
    net_worth INT,
    aghanims_scepter BOOLEAN,
    aghanims_shard BOOLEAN,
    moonshard BOOLEAN,
    hero_damage INT,
    tower_damage INT,
    hero_healing INT,
    gold INT,
    gold_spent INT,
    scaled_hero_damage INT,
    scaled_tower_damage INT,
    scaled_hero_healing INT,
    FOREIGN KEY (match_id) REFERENCES matches(id),
    FOREIGN KEY (account_id) REFERENCES players(dota2_id),
    FOREIGN KEY (item_0) REFERENCES items(id),
    FOREIGN KEY (item_1) REFERENCES items(id),
    FOREIGN KEY (item_2) REFERENCES items(id),
    FOREIGN KEY (item_3) REFERENCES items(id),
    FOREIGN KEY (item_4) REFERENCES items(id),
    FOREIGN KEY (item_5) REFERENCES items(id),
    FOREIGN KEY (backpack_0) REFERENCES items(id),
    FOREIGN KEY (backpack_1) REFERENCES items(id),
    FOREIGN KEY (backpack_2) REFERENCES items(id),
    FOREIGN KEY (item_neutral) REFERENCES items(id)
);