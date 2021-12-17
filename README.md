# CoinmarketCap-Scraper
Provides the ability to scrape coinmarketcap.com.

Script performs the following:
1. Scrapes 52 pages (page count is hard coded)
2. Sleeps in between each page read due to throttling from coinmarketcap.com
3. Scrapes the following attributes in USD:
    - Market Cap
    - 24h Volume
    - Slug name
    - Name
    - Symbol
    - Price
    - Vol to Market Cap ratio (Volume / Market Cap)
    - Max Supply
    - Circulating Supply
4.  Filters the currency to only those that meet the following criteria
    - Less than $5
    - Vol to Market Cap ratio between 10% - 50%
    - Price <> $0
5. Saves the output to a CSV file named cmp_out.csv
