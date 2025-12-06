from pysmashgg.api import run_query
import pysmashgg
import datetime
import pandas as pd
import os

smashgg_token = os.environ["SMASHGG_TOKEN"]
smash = pysmashgg.SmashGG(smashgg_token, True)
print("GOT TOKEN")

def jst_unix(y, m, d, hh=0, mm=0, ss=0):
    # JST = UTC+9
    dt = datetime.datetime(y, m, d, hh, mm, ss, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
    return int(dt.timestamp())

SHOW_BY_STATE_QUERY = """query TournamentsByPrefecture($state: String!,$page: Int!, $after: Timestamp){
        tournaments(query: {
            perPage: 32
            page: $page
            sortBy: "startAt desc"
            filter:{
                addrState: $state
                videogameIds: 1386
				afterDate :$after
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
afterdate = jst_unix(2025, 1, 1)
state_value = "Miyagi"
    
print("START")

variables = {"state": state_value, "page": page, "after": afterdate}
response = run_query(SHOW_BY_STATE_QUERY, variables, header={"Authorization": "Bearer" + smashgg_token}, auto_retry=True)
response = response["data"]["tournaments"]["nodes"]
print(response)

"""
for i in range(len(response)):
    df_tmp = pd.DataFrame.from_dict(response[i])
    df = pd.concat([df, df_tmp])
        
print("finished",page)


print(state_value)
print(df)
"""

