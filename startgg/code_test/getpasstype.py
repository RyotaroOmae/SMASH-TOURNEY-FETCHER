import pysmashgg
import pandas as pd
from pysmashgg.api import run_query
import os

smashgg_token = os.environ["SMASHGG_TOKEN"]
smash = pysmashgg.SmashGG(smashgg_token, True)

#df_tourney = pd.read_csv("tournament_list.csv")

my_slug = "8-32"
event_name = "single-tournament"

print( smash.tournament_show(my_slug) )

event_ID = smash.tournament_show_event_id(my_slug, event_name)
print("eventID",event_ID,type(event_ID))

SHOW_ENTRANTS_QUERY = """query EventStandings($eventId: ID!, $page: Int!) {
  event(id: $eventId) {
    id
    name
    standings(query: {
      perPage: 24,
      page: $page}){
      nodes {
        placement
        entrant {
          id
          name
          participants {
            player {
              id
              gamerTag
            }
          }
          seeds {
            seedNum
          }
        }
      }
    }
  }
}"""

variables = {"eventId": event_ID, "page": 1}
response = run_query(SHOW_ENTRANTS_QUERY, variables, header={"Authorization": "Bearer " + smashgg_token}, auto_retry=True)
response = response["data"]["event"]["standings"]["nodes"]
print(response)

