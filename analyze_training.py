#twitter init
try:
    import json
except ImportError:
    import simplejson as json

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

ACCESS_TOKEN = '4420601422-VlE8OQPltjU87dO6S2mmkpgFQmfPYYomS3lPXlV'
ACCESS_SECRET = 'zToR6bXhpFSuduCpQxWZmMbIiNmRCAnUB5SX9kOBAGjR8'
CONSUMER_KEY = 'fN6YLqnizJgh5S2Cn6Ee6VmvR'
CONSUMER_SECRET = 'wS10bwyYo8BH2QQpi274tqMGVUH5fYG6JKYnw3fE7f8EfkI0C2'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_stream = TwitterStream(auth=oauth)
iterator = twitter_stream.statuses.sample()

#detect language init
import detectlanguage

detectlanguage.configuration.api_key = "86e197abd2ad3eb254a40ac02cc68129"

#pickle init
import pickle

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

#dictionary init
data = load_obj("new_data")
word_totals = {}
word_freqs = {}
word_scores = {} #avg for each word

#finds average score of tweet based on word composition
def calculate_score(text, score_data):
    total = 0
    amt = 0
    words = text.split(" ")
    for w in words:
        if w in score_data:
            total += score_data[w]
            amt += 1
            
    if amt != 0:
        return total/amt
    else:
        return None

#get cumulative word scores & occurances from tweets
for text in data:
    if data[text] == "positive":
        score = 10
    elif data[text] == "negative":
        score = 1
    words = text.split(" ")
    for word in words:
        w = word.lower()
        if w in word_totals:
            word_totals[w] = word_totals[w] + score
            word_freqs[w] = word_freqs[w] + 1
        else:
            word_totals[w] = score
            word_freqs[w] = 1

#populate word_scores with average of all scores from tweets (value 1-10)
for w in word_totals:
    try:
        word = str(w)
        word_scores[word] = float(word_totals[word]) / float(word_freqs[word])
    except:
        pass

#get 10 sample tweets from twitter
tweet_list = []
tweet_count = 20
for tweet in iterator:
    try:
        text = json.loads(json.dumps((tweet)))[u'text']
        if detectlanguage.simple_detect(text) == "en":
            tweet_count -= 1
            tweet_list.append(text)
        
    except:
        pass
       
    if tweet_count <= 0:
        break

for t in tweet_list:
    print t
    print calculate_score(t, word_scores)
    print ""
