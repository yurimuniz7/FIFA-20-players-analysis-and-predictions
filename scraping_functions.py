import requests
import bs4
import time
import pandas as pd
import gc
from numpy import random
from IPython.display import clear_output

def get_player_data(player_url,to_dict=True):

    player_page = requests.get(player_url)
    soup = bs4.BeautifulSoup(player_page.text,"html.parser")
    cards = soup.find_all("div", {"class": "card-body"})
    teams_info = soup.find_all('div',{'class':'col-12 col-sm-6 col-lg-6 team'})

    info_list = list(soup.find('h5').stripped_strings)
    info_list.append(soup.find_all('a', {"class": "link-nation"})[1].text)
    info_list.append(cards[0].p.text)

    tags = cards[1].find_all('p')
    for tag in tags[:5]:
        info_list.append(list(tag.strings)[1])

    positions = ''
    for position in list(tags[5].strings)[1:]:
        positions += position + '/'

    info_list.append(positions[:-1])
    info_list.append(list(tags[6].strings)[1])
    weak_foot_stars = len(tags[7].find_all('i',{"class": "fas fa-star fa-lg"}))
    info_list.append(weak_foot_stars)
    skill_moves_stars = len(tags[8].find_all('i',{"class": "fas fa-star fa-lg"}))
    info_list.append(skill_moves_stars)

    number_teams = len(teams_info)
    if number_teams == 0:
        info_list.append(0)
        info_list.append(0)
    elif teams_info[0].h5.text.strip() == 'Free Agents':
        info_list.append(0)
        info_list.append(0)
    else:
        info_list.append(list(tags[9].strings)[1])
        info_list.append(list(tags[12].strings)[1])

# This part of the code is just meant to free memory usage (check the links below to understand the issue)
# https://stackoverflow.com/questions/11284643/python-high-memory-usage-with-beautifulsoup
# https://stackoverflow.com/questions/42608004/beautifulsoup-memory-leak
    for bs4element in tags:
        bs4element.decompose()

# Back to the scraping
    if number_teams == 2:
        if teams_info[0].h5.text.strip() == 'Free Agents':
            info_list.append(teams_info[0].h5.text.strip())
            info_list.append(teams_info[1].h5.text.strip())
        else:
            info_list.append(teams_info[1].h5.text.strip())
            info_list.append(teams_info[0].h5.text.strip())
    elif number_teams == 1:
        info_list.append(teams_info[0].h5.text.strip())
        info_list.append(0)
    else:
        info_list.append(0)
        info_list.append(0)

    for bs4element in teams_info:
        bs4element.decompose()

    for i in range(number_teams + 2,number_teams + 9):
        tags = cards[i].find_all('p')
        for tag in tags:
            info_list.append(int(tag.span.text))
            #Freeing memory
            tag.decompose()

    if len(cards) == number_teams + 9:
        info_list.append(0)
    else:
        specialities_traits = ''
        for card in cards[(number_teams + 9):]:
            for tag in card.find_all('p'):
                specialities_traits += tag.text + '/'

        specialities_traits = specialities_traits[:-1]
        info_list.append(specialities_traits)

    if to_dict:
        keys = ['name','overall','potential','nationality','description','height','weight','preferred_foot','birth_date',\
               'age','preferred_positions','work_rate','weak_foot','skill_moves','value','wage','team_club','team_nation',\
               'ball_control','dribbling','marking','side_tackle','stand_tackle','aggression','reactions','att_position',\
               'interceptions','vision','composure','crossing','short_pass','long_pass','acceleration','stamina','strength',\
               'balance','sprint_speed','agility','jumping','heading','shot_power','finishing','long_shot','curve','fk_acc',\
               'penalties','volleys','gk_positioning','gk_diving','gk_handling','gk_kicking','gk_reflexes','specialities_traits']
        player_data = dict(zip(keys,info_list))
    else:
        player_data = info_list

    # Freeing memory
    for bs4element in cards:
        bs4element.decompose()
    soup.decompose()
    gc.collect()

    return player_data

def get_players_ids(players_list_url):
    players_ids = []
    fifaindex_url = 'https://www.fifaindex.com'
    link_tag = {'href':players_list_url.split('.com')[1]}

    while bool(link_tag):
        # Adding a delay to the scraper
        time.sleep(0.5 + random.rand())
        players_list_url = fifaindex_url+link_tag['href']
        players_list_page = requests.get(players_list_url)
        soup = bs4.BeautifulSoup(players_list_page.text,"html.parser")

        for player_tag in soup.find_all(attrs={'data-playerid': True}):
            players_ids.append(player_tag['data-playerid'])

        link_tag = soup.find('a',string='Next Page')

    soup = None
    link_tag = None
    gc.collect()

    return players_ids

def generate_players_df(players_ids):
    number_of_players = len(players_ids)

    columns = ['name','overall','potential','nationality','description','height','weight','preferred_foot','birth_date',\
               'age','preferred_positions','work_rate','weak_foot','skill_moves','value','wage','team_club','team_nation',\
               'ball_control','dribbling','marking','side_tackle','stand_tackle','aggression','reactions','att_position',\
               'interceptions','vision','composure','crossing','short_pass','long_pass','acceleration','stamina','strength',\
               'balance','sprint_speed','agility','jumping','heading','shot_power','finishing','long_shot','curve','fk_acc',\
               'penalties','volleys','gk_positioning','gk_diving','gk_handling','gk_kicking','gk_reflexes','specialities_traits']
    players_df = pd.DataFrame(columns=columns)

    for i, player_id in enumerate(players_ids):
        print('{} players remaining'.format(number_of_players - i))
        # Adding a delay to the scraper (Do not scrape too fast!)
        time.sleep(1 + random.rand())
        player_url = 'https://www.fifaindex.com/player/'+str(player_id)
        players_df.loc[i] = get_player_data(player_url,to_dict=False)
        clear_output(wait=True)

    print('Done!')

    return players_df
