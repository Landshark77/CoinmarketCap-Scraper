from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time

numDataError = 0

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
pageNum = []

df = pd.DataFrame(columns = ['PageNum', 'slug', 'name', 'symbol','price', 'MarketCap', 'volume','Volume / MarketCap','Circulating Supply','Max Supply','Total Supply'])

#Load coins
for x in range(1, numPages+1):
	
	print(f'Gathering Coin data from page {x} of {numPages}')
	cmc = requests.get(f'https://coinmarketcap.com/?page={x}')
	time.sleep(1)
	soup = BeautifulSoup(cmc.content, 'html.parser')
	data = soup.find('script', id="__NEXT_DATA__",type="application/json")
	coin_data = json.loads(data.contents[0])
	listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

	#make sure the page number and the data are equal
	if x == int(coin_data['props']['initialState']['cryptocurrency']['listingLatest']['page']):
		for i in listings:
			#first need to get the column indexes of the data we want to pull back
			if type(i) == dict:
				varName = i['keysArr'].index('name')
				varMarketCap = i['keysArr'].index('quote.USD.marketCap')
				var24hrVolume = i['keysArr'].index('quote.USD.volume24h')
				varSlug = i['keysArr'].index('slug')
				varSymbol = i['keysArr'].index('symbol')
				
				#not sure why, but on a few pages they exclude maxsupply
				try:
					varMaxSupply = i['keysArr'].index('maxSupply')
				except ValueError:
					varMaxSupply = -1

				varTotalSupply = i['keysArr'].index('totalSupply')
				varCirSupply = i['keysArr'].index('circulatingSupply')
				varPrice = i['keysArr'].index('quote.USD.price')

			if type(i) == list: 
				
				if int(i[varMarketCap]) > 0: #this will export all coins with a marketcap greater than zero
					pageNum.append(x)
					market_cap.append(i[varMarketCap])
					volume.append(i[var24hrVolume])
					slug.append(i[varSlug])
					name.append(i[varName])
					symbol.append(i[varSymbol])
					price.append(i[varPrice])
					
					try:
						volcap.append(i[var24hrVolume] / i[varMarketCap]) 
					except ZeroDivisionError:
						volcap.append(0)

					cirsupply.append(i[varCirSupply])
					totsupply.append(i[varTotalSupply])
					
					if varMaxSupply > 0:
						maxsupply.append(i[varMaxSupply])
					else:
						maxsupply.append(0)
	else:
		print(f'Data not equal, skipping page {x}')
		numDataError += 1

print(f'Total Pages skipped: {numDataError}')
df['PageNum'] = pageNum
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
