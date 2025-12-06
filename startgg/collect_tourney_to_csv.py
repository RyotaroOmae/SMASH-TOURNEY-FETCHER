from pysmashgg.api import run_query
import pysmashgg
import pandas as pd
import datetime
import os

pd.set_option('display.unicode.east_asian_width',True)

smashgg_token = os.environ["SMASHGG_TOKEN"]
smash = pysmashgg.SmashGG(smashgg_token, True)
print("GOT TOKEN")

SHOW_BY_STATE_QUERY = """query TournamentsByPrefecture($state: String!,$page: Int!,$after: Timestamp!){
        tournaments(query: {
            perPage: 32
            page: $page
            sortBy: "startAt desc"
            filter:{
                addrState: $state
                videogameIds: 1386
                afterDate: $after
            }
        }) {
            nodes{
                id name
                slug
                numAttendees
                city
                startAt
                endAt
                state
            }
        }
    }"""

page = 1
df = pd.DataFrame()
backtime = 31536000 #1年前からなので
afterdate = int(datetime.datetime.now().timestamp()) - backtime

for state_value in ["青森県","Aomori","岩手県","Iwate","秋田県","Akita","宮城県","Miyagi","山形県","Yamagata","福島県","Fukushima"]:
    
    print("START")

    variables = {"state": state_value, "page": page, "after": afterdate}
    response = run_query(SHOW_BY_STATE_QUERY, variables, header={"Authorization": "Bearer" + smashgg_token}, auto_retry=True)
    #print(response)
    response = response["data"]["tournaments"]["nodes"]
    print(response)

    print("RESPONSED")

    for i in range(len(response)):
        df_tmp = pd.DataFrame(response[i].values(),index=response[i].keys()).T
        df = pd.concat([df, df_tmp])
    print("finished",state_value)
    
print(df)

dir_data = "data"
if not os.path.exists(dir_data):
    os.makedirs(dir_data)
df.to_csv(f"{dir_data}/tournament_list.csv",index=False)

print("tournament_list.csv is saved")






