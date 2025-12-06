import pysmashgg
import pandas as pd
import os

smashgg_token = os.environ["SMASHGG_TOKEN"]
print(len(smashgg_token))
smash = pysmashgg.SmashGG(smashgg_token, True)

#df_tourney = pd.read_csv("tournament_list.csv")

my_slug = "8-32"
event_name = "single-tournament"

print( smash.tournament_show(my_slug) )

eventID = smash.tournament_show_event_id(my_slug, event_name)
print("eventID",eventID)

df = pd.DataFrame()
page_max = 3

for page in range( 1, page_max + 1 ):
    while 1:
        try: #エラー対策
            entrants = smash.event_show_entrants(eventID, page)
        except:
            continue

        if len(entrants):

            df_tmp = pd.DataFrame.from_dict(entrants)
            df = pd.concat([df, df_tmp])

            page += 1

        else:
            break

df = (df
      .assign(playerId = lambda x: x.entrantPlayers.apply(lambda y: y[0]["playerId"]))
      .assign(playerTag = lambda x: x.entrantPlayers.apply(lambda y: y[0]["playerTag"]))
      .drop(columns="entrantPlayers")
     )

df.to_csv(my_slug + ".csv", index=False )

print(df)


