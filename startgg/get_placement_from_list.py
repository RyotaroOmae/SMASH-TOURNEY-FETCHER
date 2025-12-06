from pysmashgg.api import run_query
import pysmashgg
import pandas as pd
import os

pd.set_option('display.unicode.east_asian_width',True)

smashgg_token = os.environ["SMASHGG_TOKEN"]
smash = pysmashgg.SmashGG(smashgg_token, True)
print("GOT TOKEN")

#slugだけ取り出す,このcsvはcollect_tourney_to_csv.pyから得る
df = pd.read_csv("tournament_list.csv")
df_slug = df["slug"].str.replace("tournament/","")
print(df_slug.shape)

df_name = df["name"]
df_name = pd.concat([df_name,df["numAttendees"]],axis=1)

#大会のslugからeventIDを得る
EVENT_ID_QUERY = """query ($tourneySlug: String!){
        tournament(slug: $tourneySlug) {
            events {
		    	id
			}
		}
    }"""

list_res =[]

for i in range(0,len(df_slug)):

    variables = {"tourneySlug": df_slug[i]}
    response = run_query(EVENT_ID_QUERY, variables, header={"Authorization": "Bearer" + smashgg_token}, auto_retry=True)
    response = response["data"]["tournament"]["events"]
    
    list_res.append(response[0])
    df_ID = pd.DataFrame(list_res)
    print(response[0])

#print(df_ID)

#0列目が大会名,1列目がnumAttendees,2列目がeventID
df_nameID = pd.concat([df_name,df_ID], axis=1)
print("df_nameID")
print(df_nameID)

stands_name = pd.DataFrame()
stands_ID = pd.DataFrame()

#standingのデータを得る
SHOW_ENTRANTS_QUERY = """query EventStandings($eventId: ID!, $page: Int!) {
  event(id: $eventId) {
    id
    name
    standings(query: {
      perPage: 25,
      page: $page}){
      nodes {
        placement
        entrant {
          participants {
            player {
              id
              gamerTag
            }
          }
        }
      }
    }
  }
}"""


#大会ごとにentrantsのクエリを実行
for i in range(len(df_nameID)):

  df_placement = pd.DataFrame()

  #numAttendeeからページを計算
  #print(df_nameID.iloc[i,1].dtype)
  num = df_nameID.iloc[i,1]//25 + 1

  for pg in range(1, num+1):

    variables = {"eventId": str(df_nameID.iloc[i,2]), "page": str(pg)}
    response = run_query(SHOW_ENTRANTS_QUERY, variables, header={"Authorization": "Bearer" + smashgg_token}, auto_retry=True)
    response = response["data"]["event"]["standings"]["nodes"]
    #responseはリスト

    #placeだけの配列
    df_tmp = pd.DataFrame([d.get("placement") for d in response],columns=["placement"])

    #idとgamerTagだけの配列
    df_tmp_id = pd.json_normalize(response, record_path=["entrant","participants"],sep="_")
    #print(df_tmp_id)

    #上の2つ横にくっつける
    df_tmp = pd.concat([df_tmp,df_tmp_id],axis=1)

    #print(df_tmp)
    #print(response)

    #今のpageのを下にくっつける
    df_placement = pd.concat([df_placement,df_tmp],axis=0,ignore_index=True)


  tourney_name = df_nameID.iat[i,0].replace(" ","").replace("!","")

  print(df_placement)

  if df_placement is None or df_placement.empty:
      print(f"[SKIP] no placement yet: {tourney_name}")
      continue
  if "player_gamerTag" not in df_placement.columns:
      print(f"[SKIP] missing player_gamerTag: {tourney_name} cols={list(df_placement.columns)}")
      continue

  #列名を大会名にしつつ横につなげる
  stands_name = pd.concat([stands_name,df_placement.rename({"player_gamerTag":tourney_name},axis=1)[tourney_name]],axis=1)
  stands_ID   = pd.concat([stands_ID,df_placement.rename({"player_id":tourney_name},axis=1)[tourney_name]],axis=1)
  
  print(" ")

print(stands_name)
print(stands_ID)

stands_name.to_csv("data/standings_startgg_name.csv")
stands_ID.to_csv("data/standings_startgg_ID.csv")
print("csv files are saved in ./data")

