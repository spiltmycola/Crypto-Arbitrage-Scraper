# Crypto Arbitrage Scraper

- Scrapes market table from coinmarketcap.com (currently BTC)
- For every exchange pair, e.g. 'ETH/BTC', highest and lowest bid/ask is found
- Outputs json file 'db.json' with list of these pairs sorted by greatest to least price difference, currently contains sample data

Requires BeautifulSoup