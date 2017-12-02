# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import detectlanguage, pickle

#pickle wrapper functions
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

training_data = load_obj("training_data")

# auth tokens
ACCESS_TOKEN = '4420601422-VlE8OQPltjU87dO6S2mmkpgFQmfPYYomS3lPXlV'
ACCESS_SECRET = 'zToR6bXhpFSuduCpQxWZmMbIiNmRCAnUB5SX9kOBAGjR8'
CONSUMER_KEY = 'fN6YLqnizJgh5S2Cn6Ee6VmvR'
CONSUMER_SECRET = 'wS10bwyYo8BH2QQpi274tqMGVUH5fYG6JKYnw3fE7f8EfkI0C2'


detectlanguage.configuration.api_key = "86e197abd2ad3eb254a40ac02cc68129"

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_stream = TwitterStream(auth=oauth)

iterator = twitter_stream.statuses.sample()


tweet_count = 50
for tweet in iterator:
    tweet_count -= 1

    try:
        text = json.loads(json.dumps((tweet)))[u'text']
        if detectlanguage.simple_detect(text) == "en":
            ans = raw_input(text)

            if ans == "h":
                training_data[text] = "positive"
            elif ans == "s":
                training_data[text] = "negative"
            
        
    except:
        pass
       
    if tweet_count <= 0:
        break

save_obj(training_data, "training_data")
