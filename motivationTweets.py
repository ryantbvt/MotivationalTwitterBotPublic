import tweepy
import time
import random

print("Booting")

CONSUMER_KEY = 'HD3y2q1uqGeb7RWuMilO15rUi'
CONSUMER_SECRET = 'fI0CeCNiqE83kzXxzBNFLaGudUSAjV3dAB6vZCUt7QnI7VwEGu'
ACCESS_KEY = '1247728862340972544-Kkdlu1qff5acWayEbVNPi1o8nY5Pnw'
ACCESS_SECRET = '26KTUjkEa6nXVFHahrhSmbw5EahcaKh2vAD0Asrmbly3U'

#API commands
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    # DEV NOTE: use 1247996016105861120 for testing
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)

        if '#hello' in mention.full_text.lower():
            print('found #hello')
            print('responding back')
            api.update_status('hello ' + '@' + mention.user.screen_name, mention.id)

        if '#motivation' in mention.full_text.lower():
            print('found #quote')
            print('responding back')
            api.update_status('@' + mention.user.screen_name + ' ' + randomQuotesGenerator(), mention.id)

#generates random quotes
def randomQuotesGenerator():
    q = open('quotes.txt', 'r')

    q_contents = q.readlines()
    #print(q_contents)
    
    arr = []
    for i in range(0, len(q_contents) - 1):
        x = q_contents[i]
        z = len(x)
        a = x[:z - 1]
        arr.append(a)

    arr.append(q_contents[i+1])
    o = random.choice(arr)
    print(o)

    q.close
    return o
    

#add quotes to list
def addQuote():
    with open('quotes.txt', 'a') as q:
        b = True
        while b == True:
            inp = input('add a quote, if not type "no"\n')
            if inp != 'no':
                q.write(inp + '\n')
            else:
                b = False

addQuote()

#runs all the code
while True:
    print('Looking for tweets')
    reply_to_tweets()
    time.sleep(15)