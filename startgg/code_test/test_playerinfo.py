from pysmashgg import filters
from pysmashgg.p_queries import *
from pysmashgg.api import run_query
import pysmashgg
import pandas as pd
import os

pd.set_option('display.unicode.east_asian_width',True)

smashgg_token = os.environ["SMASHGG_TOKEN"]
smash = pysmashgg.SmashGG(smashgg_token, True)
print("GOT TOKEN")


PLAYER_SHOW_INFO_QUERY = """query ($playerId: ID!) {
  player(id: $playerId) {
    gamerTag
    user {
      name
      genderPronoun
      location {
        country
        state
        city
      }
    }
    rankings(videogameId: 1) {
      title
      rank
    }
  }
} """

player_id = 3128645
header={"Authorization": "Bearer" + smashgg_token}

# Shows info for a player
def show_info(player_id, header, auto_retry):
    variables = {"playerId": player_id}
    response = run_query(PLAYER_SHOW_INFO_QUERY, variables, header, auto_retry)
    data = filters.player_show_info_filter(response)
    return data

print(show_info(player_id,header,True))
