import challonge
import pandas as pd
import os

pd.set_option('display.unicode.east_asian_width',True)

username = os.environ["CHALLONGE_USER_NAME"]
APIkey = os.environ["CHALLONGE_API_KEY"]
challonge.set_credentials(username, APIkey)

#for example
URL = "https://challonge.com/ja/funbakaruby"

slug = URL.replace("https://challonge.com/ja/","")

tournament = challonge.tournaments.show(slug)
#print(tournament)

#Get list of participants by "list"
participants = challonge.participants.index(tournament['id'])
#print(participants)

list_name = [ d.get('name') for d in participants ]

list_final_rank = [ d.get('final_rank') for d in participants ]


df = pd.DataFrame({'final_rank':list_final_rank,'name':list_name})
df = df.sort_values('final_rank',ignore_index=True)


print(df)

