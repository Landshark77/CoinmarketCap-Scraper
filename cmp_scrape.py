from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time

market_cap = []
volume = []
name = []
symbol = []
slug = [] 
price = []
volcap = []
cirsupply = []
maxsupply = []

#Load coins
for x in range(1, 53):
	print(f'Gathering Coin data from page {x} of 52')
	cmc = requests.get(f'https://coinmarketcap.com/?page={x}')
	time.sleep(0.5)
	soup = BeautifulSoup(cmc.content, 'html.parser')
	data = soup.find('script', id="__NEXT_DATA__",type="application/json")
	coin_data = json.loads(data.contents[0])
	listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
	for i in listings:
		#if i['quote']['USD']['price'] < 5 and i['quote']['USD']['marketCap'] > 0 and i['quote']['USD']['price'] >= 0.01 and i['quote']['USD']['volume24h'] >= 1000000:
		if i['quote']['USD']['marketCap'] > 0 and i['quote']['USD']['price'] >= 0.01: #and i['quote']['USD']['volume24h'] >= 1000000:
			#if (i['quote']['USD']['volume24h'] / i['quote']['USD']['marketCap'] >= .1) and (i['quote']['USD']['volume24h'] / i['quote']['USD']['marketCap'] <= .5):
				market_cap.append(i['quote']['USD']['marketCap'])
				volume.append(i['quote']['USD']['volume24h'])
				slug.append(i['slug'])
				name.append(i['name'])
				symbol.append(i['symbol'])
				price.append(i['quote']['USD']['price'])
				volcap.append(i['quote']['USD']['volume24h'] / i['quote']['USD']['marketCap']) 
				cirsupply.append(i['circulatingSupply'])
				
				try:
					maxsupply.append(i['maxSupply'])
				except KeyError:
					maxsupply.append(0)

df = pd.DataFrame(columns = ['slug', 'name', 'symbol','price', 'MarketCap', 'volume','Volume / MarketCap','Circulating Supply','Max Supply'])
df['slug'] = slug
df['name'] = name
df['symbol'] = symbol
df['price'] = price
df['MarketCap'] = market_cap
df['volume'] = volume
df['Volume / MarketCap'] = volcap
df['Circulating Supply'] = cirsupply
df['Max Supply'] = maxsupply
df.to_csv('cmp_out.csv',index = False)
