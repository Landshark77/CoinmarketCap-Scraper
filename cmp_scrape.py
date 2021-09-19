from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time

#Update variable to match total number of pages found on coinmarketcap
numPages = 67

#objectes for pandas
market_cap = []
volume = []
name = []
symbol = []
slug = [] 
price = []
volcap = []
cirsupply = []
maxsupply = []
totsupply = []

#variables for array
varName = 15
varMarketCap = 55
var24hrVolume = 66
varSlug = 125
varSymbol = 126
varMaxSupply = 14
varTotalSupply = 127
varCirSupply = 2
varPrice = 64

#Load coins
for x in range(1, numPages):
	print(f'Gathering Coin data from page {x} of {numPages-1}')
	cmc = requests.get(f'https://coinmarketcap.com/?page={x}')
	time.sleep(0.5)
	soup = BeautifulSoup(cmc.content, 'html.parser')
	data = soup.find('script', id="__NEXT_DATA__",type="application/json")
	coin_data = json.loads(data.contents[0])
	listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
	for i in listings:
		if type(i) == list: 
			if i[varMarketCap] > 0: #this will export all coins with a marketcap greater than zero
				market_cap.append(i[varMarketCap])
				volume.append(i[var24hrVolume])
				slug.append(i[varSlug])
				name.append(i[varName])
				symbol.append(i[varSymbol])
				price.append(i[varPrice])
				volcap.append(i[var24hrVolume] / i[varMarketCap]) 
				cirsupply.append(i[varCirSupply])
				totsupply.append(i[varTotalSupply])

				try:
					maxsupply.append(i[varMaxSupply])
				except KeyError:
					maxsupply.append(0)

df = pd.DataFrame(columns = ['slug', 'name', 'symbol','price', 'MarketCap', 'volume','Volume / MarketCap','Circulating Supply','Max Supply','Total Supply'])
df['slug'] = slug
df['name'] = name
df['symbol'] = symbol
df['price'] = price
df['MarketCap'] = market_cap
df['volume'] = volume
df['Volume / MarketCap'] = volcap
df['Circulating Supply'] = cirsupply
df['Max Supply'] = maxsupply
df['Total Supply'] = totsupply
df.to_csv('cmp_out.csv',index = False)
