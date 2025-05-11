import requests
import json
import csv

code_to_weather = {
    '100': '晴れ',
    '101': '晴れ時々曇',
    '102': '晴れ一時雨',
    '200': '曇り',
    '201': '曇り時々晴れ',
    '202': '曇り一時雨',
    '212': '曇りのち一時雨',
    '213': '曇り後雨',
    '214': '曇りのち雨',
    '300': '雨',
    '313': '雨のち曇',
    '400': '雪',
    '500': '雷雨'
    # 必要に応じて他のコードを追加
}


url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/230000.json'

res = requests.get(url)
res.encoding = 'utf-8'
data = json.loads(res.text)

# 天気・降水確率・信頼度 → 愛知県エリア
weather_area = data[1]['timeSeries'][0]['areas'][0]
dates = data[1]['timeSeries'][0]['timeDefines']
weather_codes = weather_area['weatherCodes']
pops = weather_area['pops']
reliabilities = weather_area.get('reliabilities',[])

# 気温 → 名古屋エリア

temp_area = data[1]['timeSeries'][1]['areas'][0]

temps_max = temp_area['tempsMax']

temps_min = temp_area['tempsMin']

weather_data = []
for i in range(len(dates)):

    date = dates[i][:10]

    code = str(weather_codes[i]) if i < len(weather_codes) else ''

    weather = code_to_weather.get(code, f"コード:{code}")

    tmax = temps_max[i] if i < len(temps_max) else ''

    tmin = temps_min[i] if i < len(temps_min) else ''
    
    pop = pops[i] if i < len(pops) else ''

    reliability =reliabilities[i] if i < len(reliabilities) else ''

    weather_data.append([date,weather,tmax,tmin,pop,reliability])

with open('nagoya_weekly_weather.csv','w',newline='',encoding='utf-8-sig') as f:
    writer =csv.writer(f)
    writer.writerow(['日付', '天気', '最高気温', '最低気温', '降水確率', '信頼度'])
    writer.writerows(weather_data)

print("'nagoya_weekly_weather.csv' に名古屋市の週間予報を保存")