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
price = []
volcap = []

intCoinCount = 0

#Load coins
for x in range(1, 42):
	print(f'Building Coin list page {x} of 41')
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
#		coins[str(i['id'])] = i['slug']
		if i['quote']['USD']['price'] < 5 and i['quote']['USD']['market_cap'] > 0 and i['quote']['USD']['price'] > 0:
			if (i['quote']['USD']['volume_24h'] / i['quote']['USD']['market_cap'] >= .1) and (i['quote']['USD']['volume_24h'] / i['quote']['USD']['market_cap'] <= .5):
				market_cap.append(i['quote']['USD']['market_cap'])
				volume.append(i['quote']['USD']['volume_24h'])
				slug.append(i['slug'])
				name.append(i['name'])
				symbol.append(i['symbol'])
				price.append(i['quote']['USD']['price'])
				volcap.append(i['quote']['USD']['volume_24h'] / i['quote']['USD']['market_cap']) 


#get data for each coin
#for i in coins:
#	intCoinCount += 1
#	page = requests.get(f'https://coinmarketcap.com/currencies/{coins[i]}/historical-data/')
#	print(f'Retrieving stats {intCoinCount} of {len(coins)} for >> {coins[i]}')
#	time.sleep(1) #must sleep to avoid throttling by website.  increase as needed.
#	soup = BeautifulSoup(page.content, 'html.parser')
#	data = soup.find('script', id="__NEXT_DATA__",type="application/json")
#	coin_data = json.loads(data.contents[0])
#	quotes = coin_data['props']['initialProps']['pageProps']['info']
#	if (quotes['status'] == "active") and (quotes['statistics']['price'] < 5):
#		market_cap.append(quotes['statistics']['marketCap'])
#		volume.append(quotes['statistics']['volumeYesterday'])
#		slug.append(coins[i])
#		name.append(quotes['name'])
#		symbol.append(quotes['symbol'])
#		category.append(quotes['category'])
#		price.append(quotes['statistics']['price'])
#		if quotes['statistics']['marketCap'] > 0:
#			volcap.append(quotes['statistics']['volumeYesterday'] / quotes['statistics']['marketCap']) 
#		else:
#			volcap.append(0)

df = pd.DataFrame(columns = ['slug', 'name', 'symbol','price', 'MarketCap', 'volume','Volume / MarketCap'])
df['slug'] = slug
df['name'] = name
df['symbol'] = symbol
df['price'] = price
df['MarketCap'] = market_cap
df['volume'] = volume
df['Volume / MarketCap'] = volcap 
df.to_csv('cmp_out.csv',index = False)