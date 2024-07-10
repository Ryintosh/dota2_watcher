import requests
import modules.imagegenerator as ig
import modules.secrets as secrets


def update_discord(matchData,image):
    message = {"content":f"https://www.dotabuff.com/matches/{matchData.match_id}"}
    requests.post(secrets.load_secret_config("webhooks")["DISCORD_WEBHOOK"],data=message,files=image)