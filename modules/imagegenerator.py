import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import datetime
import modules.mysql as mysql
from modules.player import Player
import modules.steamapi as dota2


# creates an image
def create_image(match_summary):
    # Create a new image with white background
    width, height = 1920, 1080
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    image.paste(ImageEnhance.Brightness(Image.open("images/dota2background.jpg")).enhance(0.5),(0,0))
    # Define fonts and colors
    title_font = ImageFont.truetype('fonts/arialbd.ttf', size=36)
    text_font = ImageFont.truetype('fonts/arialbd.ttf', size=24)
    title_color = 'white'
    text_color = 'white'
    hero_picture_size = (192, 96)
    item_picture_size = (int(hero_picture_size[0] / 2), int(hero_picture_size[1] / 2))

    # Draw text on image
    x, y = 0, 0
    if match_summary.radiant_win == 0:
        draw.text((int(width / 2) - int(draw.textlength("Dire Won", font=title_font)/2), 100), f"Dire Won", font=title_font, fill=text_color)
    else:
        draw.text((int(width / 2) - int(draw.textlength("Radiant Won", font=title_font)/2), 100), f"Radiant Won", font=title_font, fill=text_color)
        
    y += 50
    draw.text((int(width / 2) - int(draw.textlength(f"{str(datetime.timedelta(seconds=match_summary.duration))}", font=text_font)/2), 150), f"{str(datetime.timedelta(seconds=match_summary.duration))}", font=text_font, fill=text_color)
    y += 30

    direx = width
    draw.text((x, y), "Radiant Team", font=title_font, fill=title_color)
    draw.text((direx-draw.textlength("Dire Team", font=title_font), y), "Dire Team:", font=title_font, fill=title_color)

    radianty = y + 50
    direy = y + 50  

    
    def items_image(itemId,location):
        if itemId != 0:
            image.paste(Image.open(io.BytesIO(requests.get(f'https://cdn.dota2.com{str(mysql.select_db(f"SELECT img FROM items WHERE id = {itemId}")[0][0])}').content)).resize(item_picture_size),(location))

    def items_consumed_image(player,heroLocation):
        if player.aghanims_scepter == 1: 
            image.paste(Image.open(io.BytesIO(requests.get(f'https://cdn.dota2.com{str(mysql.select_db(f"SELECT img FROM items WHERE id = 108")[0][0])}').content)).resize((int(hero_picture_size[0]/3),int(hero_picture_size[1]/3))),(heroLocation[0],heroLocation[1]+hero_picture_size[1]))
        if player.aghanims_shard == 1: 
            image.paste(Image.open(io.BytesIO(requests.get(f'https://cdn.dota2.com{str(mysql.select_db(f"SELECT img FROM items WHERE id = 609")[0][0])}').content)).resize((int(hero_picture_size[0]/3),int(hero_picture_size[1]/3))),(heroLocation[0]+int(hero_picture_size[0]/3),heroLocation[1]+hero_picture_size[1]))
        if player.moonshard == 1: 
            image.paste(Image.open(io.BytesIO(requests.get(f'https://cdn.dota2.com{str(mysql.select_db(f"SELECT img FROM items WHERE id = 247")[0][0])}').content)).resize((int(hero_picture_size[0]/3),int(hero_picture_size[1]/3))),(heroLocation[0]+int(hero_picture_size[0]/3)*2,heroLocation[1]+hero_picture_size[1]))


    for player in match_summary.players:
        playerMetaData = dota2.get_player_info(player.account_id+76561197960265728)
        if player.team_number == 0:
            if playerMetaData != None:    
                draw.text((x, radianty), f'{playerMetaData["personaname"]}', font=text_font, fill=title_color)
            else:
                draw.text((x, radianty), f'Unknown Player', font=text_font, fill=title_color)
            radianty += 30
            image.paste(Image.open(io.BytesIO(requests.get(f'https://cdn.dota2.com{str(mysql.select_db(f"SELECT img FROM heroes WHERE id = {player.hero_id}")[0][0])}').content)).resize(hero_picture_size),(x,radianty))
            items_consumed_image(player,(x,radianty))
            radianty += 50 + hero_picture_size[1]

            heroIconLocation = (x,radianty-50 -hero_picture_size[1])

            heroIconLocation = (heroIconLocation[0] + (hero_picture_size[0]), heroIconLocation[1])
            items_image(player.item_0,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] + item_picture_size[0], heroIconLocation[1])
            items_image(player.item_1,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] + item_picture_size[0], heroIconLocation[1])
            items_image(player.item_2,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] - (item_picture_size[0]*2), heroIconLocation[1] + item_picture_size[1])

            items_image(player.item_3,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] + item_picture_size[0], heroIconLocation[1])
            items_image(player.item_4,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] + item_picture_size[0], heroIconLocation[1])
            items_image(player.item_5,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] - (item_picture_size[0]*2), heroIconLocation[1] + item_picture_size[1])

            items_image(player.backpack_0,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] + item_picture_size[0], heroIconLocation[1])
            items_image(player.backpack_1,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] + item_picture_size[0], heroIconLocation[1])
            items_image(player.backpack_2,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] + item_picture_size[0], heroIconLocation[1] - int((hero_picture_size[1]/2) +(item_picture_size[1]/2)))
            items_image(player.item_neutral,heroIconLocation)

            # Setting Networth and KDA
            heroIconLocation = (heroIconLocation[0]+item_picture_size[0]+30, heroIconLocation[1]-(item_picture_size[1]/2))
            draw.text(heroIconLocation, f'KDA: {player.kills}/{player.deaths}/{player.assists}', font=text_font, fill=title_color)
            heroIconLocation = (heroIconLocation[0], heroIconLocation[1]+ (item_picture_size[1]/2))
            draw.text(heroIconLocation, f'NETWORTH: {player.net_worth}', font=text_font, fill=title_color)
            heroIconLocation = (heroIconLocation[0], heroIconLocation[1]+ (item_picture_size[1]/2))
            draw.text(heroIconLocation, f'HERO DAMAGE: {player.hero_damage}', font=text_font, fill=title_color)            
            heroIconLocation = (heroIconLocation[0], heroIconLocation[1]+ (item_picture_size[1]/2))
            draw.text(heroIconLocation, f'LAST HITS / DENIES: {player.last_hits}/{player.denies}', font=text_font, fill=title_color)            

            radianty += 5
        else:
            direx = width
            if playerMetaData != None:
                draw.text((direx-draw.textlength(f'{playerMetaData["personaname"]}',font=text_font), direy), f'{playerMetaData["personaname"]}', font=text_font, fill=title_color)
            else:
                draw.text((direx-draw.textlength('Unknown',font=text_font), direy), f'Unknown Player', font=text_font, fill=title_color)
            direy += 30
            image.paste(Image.open(io.BytesIO(requests.get(f'https://cdn.dota2.com{str(mysql.select_db(f"SELECT img FROM heroes WHERE id = {player.hero_id}")[0][0])}').content)).resize(hero_picture_size),(direx-hero_picture_size[0],direy))
            items_consumed_image(player,(direx-hero_picture_size[0],direy))
            direy += 50 + hero_picture_size[1]

            # Setting item images relative to
            heroIconLocation = (direx,direy-50-hero_picture_size[1])

            heroIconLocation = (heroIconLocation[0] - (hero_picture_size[0] + item_picture_size[0]), heroIconLocation[1])
            items_image(player.item_0,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] - item_picture_size[0], heroIconLocation[1])
            items_image(player.item_1,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] - item_picture_size[0], heroIconLocation[1])
            items_image(player.item_2,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] + (item_picture_size[0]*2), heroIconLocation[1] + item_picture_size[1])

            items_image(player.item_3,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] - item_picture_size[0], heroIconLocation[1])
            items_image(player.item_4,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] - item_picture_size[0], heroIconLocation[1])
            items_image(player.item_5,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] + (item_picture_size[0]*2), heroIconLocation[1] + item_picture_size[1])

            items_image(player.backpack_0,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] - item_picture_size[0], heroIconLocation[1])
            items_image(player.backpack_1,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] - item_picture_size[0], heroIconLocation[1])
            items_image(player.backpack_2,heroIconLocation)
            heroIconLocation = (heroIconLocation[0] - item_picture_size[0], heroIconLocation[1] - int((hero_picture_size[1]/2) +(item_picture_size[1]/2)))
            items_image(player.item_neutral,heroIconLocation)

            # Setting Networth and KDA
            heroIconLocation = (heroIconLocation[0] - 30, heroIconLocation[1]-(item_picture_size[1]/2))
            draw.text(((heroIconLocation[0])-draw.textlength(f'KDA: {player.kills}/{player.deaths}/{player.assists}',font=text_font), heroIconLocation[1]), f'KDA: {player.kills}/{player.deaths}/{player.assists}', font=text_font, fill=title_color)
            heroIconLocation = (heroIconLocation[0], heroIconLocation[1]+ (item_picture_size[1]/2))
            draw.text(((heroIconLocation[0])-draw.textlength(f'NETWORTH: {player.net_worth}',font=text_font), heroIconLocation[1]), f'NETWORTH: {player.net_worth}', font=text_font, fill=title_color)
            heroIconLocation = (heroIconLocation[0], heroIconLocation[1]+ (item_picture_size[1]/2))
            draw.text(((heroIconLocation[0])-draw.textlength(f'HERO DAMAGE: {player.hero_damage}',font=text_font), heroIconLocation[1]), f'HERO DAMAGE: {player.hero_damage}', font=text_font, fill=title_color)
            heroIconLocation = (heroIconLocation[0], heroIconLocation[1]+ (item_picture_size[1]/2))
            draw.text(((heroIconLocation[0])-draw.textlength(f'LAST HITS / DENIES: {player.last_hits}/{player.denies}',font=text_font), heroIconLocation[1]), f'LAST HITS / DENIES: {player.last_hits}/{player.denies}', font=text_font, fill=title_color)                        
            direy += 5

    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    files = {'file': ('match_summary.png', image_bytes, 'image/png')}

    return files