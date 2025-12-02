#First: Prepare tourneylist_challonge.csv

import challonge
import pandas as pd
import os

pd.set_option('display.unicode.east_asian_width',True)

username = os.environ["CHALLONGE_USER_NAME"]
APIkey = os.environ["CHALLONGE_API_KEY"]
challonge.set_credentials(username, APIkey)

tlist = pd.read_csv("tourneylist_challonge.csv")

errortlist = []

stands = pd.DataFrame()

for index,URL in enumerate(tlist["URL"]):

    tourney_name = tlist.iat[index,0]

    try:
        slug = URL.replace("https://challonge.com/ja/","")

        tournament = challonge.tournaments.show(slug)
        print("slug:",slug)

        #Get list of participants by "list"
        participants = challonge.participants.index(tournament['id'])
        #print(participants)

        list_name = [ d.get('name') for d in participants ]

        list_final_rank = [ d.get('final_rank') for d in participants ]


        df = pd.DataFrame({'final_rank':list_final_rank,'name':list_name})
        df = df.sort_values('final_rank',ignore_index=True)

        #列名を大会名に変更 tlistから抽出
        
        df = df.rename(columns={"name":tourney_name})

        print(df)


        stands = pd.concat([stands,df[tourney_name]],axis=1)

    except Exception as e:

        print(f"An error occurred: {e}")
        
        errortlist.append(tourney_name)

print(" ")
print(stands)
print(errortlist)

stands.to_csv("standings_challonge.csv")

