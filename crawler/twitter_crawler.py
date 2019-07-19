from tweepy import Stream

from tweepy import OAuthHandler

from tweepy.streaming import StreamListener

GEOBOX_BHAM = [-2.0336485,52.381053,-1.7288577,52.6087058]

customer_key = "9TrIboUD3Ato8fCkA1unnkTaz"
customer_secrete = "40hDJNHFwG7ZsrYqdNBwlNOBPdpXP6QUR3UzP2iAjjlAnugGIx"

access_token = "1124943135606370306-B3VEQwfh5je2wtWenWpmJ45pKX4KEY"
access_token_secrete = "yvIEgCSF9Qppyd2OkeZoSN53pHjZIzfdWJQFngwYKiKas"

class listener(StreamListener):

    def on_data(self, data):
        try:
            print(data)
            return True
        except BaseException as e:
            print('failed on data,', str(e))

    def on_error(self, status):
        print(status)

auth = OAuthHandler(customer_key, customer_secrete)

auth.set_access_token(access_token, access_token_secrete)

twitterStream = Stream(auth, listener())

#twitterStream.filter(track=["mac"])
twitterStream.filter(locations = GEOBOX_BHAM)



