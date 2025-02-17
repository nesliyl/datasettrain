import json
import requests
import time


API_KEY = "e4528cc0f7ce62599cc39b2aabd7aa9f"


FIELDS = "fields"


with open("permalinks.json", "r", encoding="utf-8") as file:
    data = json.load(file)


permalinks = [link.replace("organization/", "") for link in data]
error_permalinks = []

results = []


for index, perma_link in enumerate(permalinks):

    api_url = f"https://api.crunchbase.com/api/v4/entities/organizations/{perma_link}?user_key={API_KEY}&card_ids={FIELDS}"

    print(api_url)

    try:
        response = requests.get(api_url)
        response_data = response.json()

        props = response_data.get("properties", {})
        cards = response_data.get("cards", {})

      
        permalink = props.get("identifier", {}).get("permalink", "")
        short_description = cards.get("fields", {}).get("short_description", "")

       
        results.append({
            "permalink": permalink,
            "short_description": short_description
        })

        print(f"{index + 1}/{len(permalinks)} - {permalink}: Veri alındı.")

    except Exception as e:
        print(e)
        print(f"Hata oluştu: {perma_link} -> {str(e)}")
        error_permalinks.append(perma_link)  # Hata listesine ekle

    
    time.sleep(1)  


output_filename = "crunchbase_filtered_results.json"
error_filename = "crunchbase_errors.json"

with open(output_filename, "w", encoding="utf-8") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)

with open(error_filename, "w", encoding="utf-8") as error_file:
    json.dump({"error_permalinks": error_permalinks}, error_file, ensure_ascii=False, indent=4)

print(f"İşlem tamamlandı! Veriler '{output_filename}' dosyasına, hatalar '{error_filename}' dosyasına kaydedildi.")
