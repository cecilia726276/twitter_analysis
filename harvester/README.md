## Harvester <br>
Due to the request limit of twitter Search API, we applied for three keys for crawling on the twitter apps website. One of the keys is used to crawl current data 
and two of the keys used to crawl historical data<br>
The key words we crawled are stored in fastfood.txt. Use Streaming API to crawl current data and Store the crawled real-time data into the current_twitter
table of couchdb(current_crawling.py). Use Search API to crawl historical data(historical_crawling1.py and historical_crawling2.py). Two files crawling historical 
data respectively crawl half of the key words in the fastfood file and then Store the historical data crawled into the historical_twitter table of couchdb.
