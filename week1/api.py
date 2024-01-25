import requests
import pandas as pd

url = "https://api.spacexdata.com/v4/launches/past"

response = requests.get(url)

data = pd.json_normalize(response.json())

# print(data["static_fire_date_utc"])

print(data.columns)
print(data[data['BoosterVersion']])
