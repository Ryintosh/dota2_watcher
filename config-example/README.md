# Configuration and Secret Management
You will need five files in a new directory named /config:
- webhooks.json
- database.json
- keys.json
- players.json
- database_password.txt

These values will be used within the application and the database_password.txt will set the password for the mysql database. Below will be examples of what you should do:

## webhooks.json
```json
{
    "DISCORD_WEBHOOK":"discord webhook here"
}
```
## database.json
```json
{
    "MYSQL_HOST":"mysql",
    "MYSQL_DATABASE":"dota2",
    "MYSQL_USER":"root",
    "MYSQL_PASSWORD":"password",
    "MYSQL_PORT":3306
}

```

## keys.json
```json
{
    "STEAM_KEY":"steam_developer_api_key"
}
```

## players.json
This is used to track certain players in their matches
```json
{
    "STEAM_IDS":[
        1231412411,
        1241241242,
        12532423
    ]
}
```

## database_password.txt
```
password
```