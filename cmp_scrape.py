from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time

coins = {}

market_cap = []
volume = []
timestamp = []
name = []
symbol = []
slug = []
category = []
price = []
volcap = []

#Load coins
for x in range(41):
	print(f'Retrieving Coin list page {i} of {range(2)}')
	if x == 1: 
		cmc = requests.get('https://coinmarketcap.com/')
	else:
		cmc = requests.get(f'https://coinmarketcap.com/?page={x}')
	time.sleep(0.5)
	soup = BeautifulSoup(cmc.content, 'html.parser')
	data = soup.find('script', id="__NEXT_DATA__",type="application/json")
	coin_data = json.loads(data.contents[0])
	listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
	for i in listings:
		coins[str(i['id'])] = i['slug']

#get data for each coin
for i in coins:
	page = requests.get(f'https://coinmarketcap.com/currencies/{coins[i]}/historical-data/')
	print(f'Retrieving stats {i} of {len(coins)} -- {coins[i]}')
	time.sleep(1)
	soup = BeautifulSoup(page.content, 'html.parser')
	data = soup.find('script', id="__NEXT_DATA__",type="application/json")
	coin_data = json.loads(data.contents[0])
	quotes = coin_data['props']['initialProps']['pageProps']['info']
	if (quotes['status'] == "active") and (quotes['statistics']['volumeYesterday'] / quotes['statistics']['marketCap'] >= 0.1) and \
	   (quotes['statistics']['volumeYesterday'] / quotes['statistics']['marketCap'] <= 0.5) and (quotes['statistics']['price'] <= 5 ):
		market_cap.append(quotes['statistics']['marketCap'])
		volume.append(quotes['statistics']['volumeYesterday'])
		slug.append(coins[i])
		name.append(quotes['name'])
		symbol.append(quotes['symbol'])
		category.append(quotes['category'])
		price.append(quotes['statistics']['price'])
		volcap.append(quotes['statistics']['volumeYesterday'] / quotes['statistics']['marketCap']) 

df = pd.DataFrame(columns = ['slug', 'name', 'symbol','price', 'MarketCap', 'volume','Volume / MarketCap', 'category'])
df['slug'] = slug
df['name'] = name
df['symbol'] = symbol
df['price'] = price
df['MarketCap'] = market_cap
df['volume'] = volume
df['Volume / MarketCap'] = volcap 
df['category'] = category
df.to_csv('cmp_out.csv',index = False)