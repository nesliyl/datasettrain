import pandas as pd
import json


csv_file = "startupdataset.csv"
json_file = "crunchbase_filtered_results.json"


df = pd.read_csv(csv_file)


with open(json_file, "r", encoding="utf-8") as f:
    json_data = json.load(f)


json_dict = {f"/organization/{item['permalink']}": item["short_description"] for item in json_data}


for index, row in df.iterrows():
    if pd.isna(row["category_list"]) and row["permalink"] in json_dict:
        df.at[index, "category_list"] = json_dict[row["permalink"]]

df.to_csv("updated_startupdataset.csv", index=False)

print("Güncelleme tamamlandı. Yeni dosya: updated_startupdataset.csv")